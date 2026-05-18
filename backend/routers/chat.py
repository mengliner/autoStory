from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas import ChatRequest
from chat_service import chat_stream

router = APIRouter()


@router.post("/chat/{project_id}")
async def chat(project_id: int, req: ChatRequest, db: Session = Depends(get_db)):
    history = []  # MVP: history not yet passed from frontend, maintained by backend

    async def event_stream():
        async for event in chat_stream(project_id, req.message, history, db):
            yield event

    return StreamingResponse(event_stream(), media_type="text/event-stream")
