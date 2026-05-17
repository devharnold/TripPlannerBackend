from fastapi import APIRouter, HTTPException
from datetime import datetime
import platform

from app.memory.chat_memory import ChatMemory
from app.memory.vector_store import VectorStore

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/status")
async def system_status():
    return {
        "status": "Operational",
        "timestamp": datetime.utcnow().isoformat(),
        "python_version": platform.python_version()
    }

@router.get("/memory/chat/{user_id}")
async def inspect_chat_memory(user_id: str):
    history = await ChatMemory.get_history(user_id)
    return {
        "user_id": user_id,
        "messages_count": len(history),
        "history": history
    }

@router.get("/memory/vector/{user_id}")
async def inspect_vector_memory(user_id: str, query: str = "travel preferences"):
    results = await VectorStore.search_trip_context(user_id=user_id, query=query)
    return {"user_id": user_id, "vector_results": results}

@router.delete("/memory/{user_id}")
async def clear_user_memory(user_id: str):
    await ChatMemory.clear_history(user_id)
    await VectorStore.clear_user_context(user_id)
    return {"message": f"Memory cleared for {user_id}"}

@router.get("/metrics")
async def basic_metrics():
    return {
        "service": "Trip Planner Agent",
        "uptime_rtatus": "running",
        "agents": [
            "FlightAgent",
            "HotelAgent",
            "ActivityAgent",
            "BudgetAgent",
            "PlannerAgent"
        ]
    }