from anthropic import Anthropic
from config import ANTHROPIC_API_KEY, ANTHROPIC_BASE_URL, ANTHROPIC_MODEL
from tools import TOOLS

client = Anthropic(api_key=ANTHROPIC_API_KEY, base_url=ANTHROPIC_BASE_URL)

SYSTEM_PROMPT = """你是一个专业的小说创作助手。你的职责是帮助用户创作小说，管理故事的大纲、角色、世界观、伏笔，以及撰写章节正文。

## 工作原则
1. 先理解用户的创作意图，再通过工具调用来操作结构化数据
2. 创作内容时始终考虑与已有设定的连贯性
3. 当用户要求生成多个方案时，使用 save_candidates 暂存不同版本
4. 用户确认某个版本后，使用 confirm_candidate 写入正式表
5. 每次操作后，简要总结变更内容
6. 主动提醒用户当前的伏笔状态，帮助埋入和回收

## 工具使用指南
- 创建设定时，先查相关角色/章节是否已存在，用已有 ID 关联
- 生成章节正文时，先检查关联的大纲节点是否存在，不存在则先创建大纲
- 伏笔埋入时关联当前章节，回收时填写 resolved_chapter_id 和 resolved_note
- 大纲节点 parent_id=0 表示根级节点（卷）
- 角色 attributes 字段可以自由存放外貌、年龄、能力等扩展信息"""


def chat_with_tools(state_summary: str, messages: list[dict]) -> tuple:
    """调用 LLM，返回 (text_content, tool_calls)"""
    system = f"{SYSTEM_PROMPT}\n\n当前故事状态：\n{state_summary}"

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=4096,
        system=system,
        tools=TOOLS,
        messages=messages
    )

    text = ""
    tool_calls = []

    for block in response.content:
        if block.type == "text":
            text += block.text
        elif block.type == "tool_use":
            tool_calls.append({
                "id": block.id,
                "name": block.name,
                "input": block.input
            })

    return text, tool_calls


def continue_with_tool_result(state_summary: str, messages: list[dict], tool_results: list[dict]) -> tuple:
    """将工具执行结果发回 LLM，继续对话"""
    assistant_content = []
    for tr in tool_results:
        assistant_content.append({
            "type": "tool_result",
            "tool_use_id": tr["id"],
            "content": str(tr["result"])
        })

    messages.append({"role": "user", "content": assistant_content})

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=4096,
        system=f"{SYSTEM_PROMPT}\n\n当前故事状态：\n{state_summary}",
        tools=TOOLS,
        messages=messages
    )

    text = ""
    tool_calls = []

    for block in response.content:
        if block.type == "text":
            text += block.text
        elif block.type == "tool_use":
            tool_calls.append({
                "id": block.id,
                "name": block.name,
                "input": block.input
            })

    return text, tool_calls
