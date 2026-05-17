from fastapi import APIRouter

from app.memory.chat_memory import ChatMemory
from app.memory.vector_store import VectorStore

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/history/{user_id}")
async def get_chat_history(user_id: str):
    history = await ChatMemory.get_history(user_id)
    return {"user_id": user_id, "history": history}

@router.delete("/history/{user_id}")
async def clear_chat_history(user_id: str):
    await ChatMemory.clear_history(user_id)
    await VectorStore.clear_user_context(user_id)
    return {"message": "Chat history cleared"}
