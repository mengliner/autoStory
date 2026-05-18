import json
from typing import AsyncGenerator
from sqlalchemy.orm import Session
from llm_service import chat_with_tools, continue_with_tool_result
from tool_executor import execute_tool, build_state_summary


async def chat_stream(project_id: int, user_message: str, history: list[dict], db: Session) -> AsyncGenerator[str, None]:
    """SSE stream generator, yields SSE formatted strings"""
    state_summary = build_state_summary(project_id, db)

    messages = history + [{"role": "user", "content": user_message}]

    text, tool_calls = chat_with_tools(state_summary, messages)

    if text:
        yield f"event: text\ndata: {json.dumps({'delta': text}, ensure_ascii=False)}\n\n"

    rounds = 0
    while tool_calls and rounds < 5:
        results = []
        for tc in tool_calls:
            try:
                result = execute_tool(tc["name"], tc["input"], project_id, db)
            except Exception as e:
                result = {"success": False, "data": None, "table": "", "action": "error", "message": str(e)}

            results.append({"id": tc["id"], "name": tc["name"], "result": result})

            yield f"event: tool_call\ndata: {json.dumps({'tool': tc['name'], 'status': 'done', 'input': tc['input'], 'result': result}, ensure_ascii=False, default=str)}\n\n"

            if result.get("success") and result.get("action") in ("create", "update", "confirm"):
                yield f"event: state_patch\ndata: {json.dumps({'table': result.get('table', ''), 'action': result.get('action', ''), 'data': result.get('data', {})}, ensure_ascii=False, default=str)}\n\n"

        messages.append({"role": "assistant", "content": [{"type": "text", "text": text}] + [
            {"type": "tool_use", "id": tc["id"], "name": tc["name"], "input": tc["input"]}
            for tc in tool_calls
        ]})

        text, tool_calls = continue_with_tool_result(build_state_summary(project_id, db), messages, results)
        if text:
            yield f"event: text\ndata: {json.dumps({'delta': text}, ensure_ascii=False)}\n\n"
        rounds += 1

    yield f"event: done\ndata: {json.dumps({'status': 'complete'})}\n\n"
