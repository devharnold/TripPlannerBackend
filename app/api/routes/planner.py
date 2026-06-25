from fastapi import APIRouter, HTTPException
from app.models import TripRequest

from app.orchestrator.workflow import TripWorkflow
from app.memory.chat_memory import ChatMemory
from app.memory.vector_store import VectorStore

router = APIRouter(prefix="/planner", tags=["Planner"])

workflow = TripWorkflow()

@router.post("/chat")
async def generate_trip(request: TripRequest):
    try:
        await ChatMemory.add_message(
            user_id=request.user_id,
            role="user",
            content=(f"Trip request to {request.destination}")
        )
        
        preferences = {
            "origin": request.origin,
            "destination": request.destination,
            "depature_date": request.depature_date,
            "budget": request.budget,
            "interests": request.interests,
            "additional_prompt": request.additional_prompt
        }

        result = await workflow.generate_trip(preferences=preferences)
        if result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=result["message"]
            )
        
        await VectorStore.save_trip_context(
            user_id=request.user_id,
            context=str(preferences)
        )

        await ChatMemory.add_message(
            user_id=request.user_id,
            role="assistant",
            content=str(result["trip"])
        )

        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))