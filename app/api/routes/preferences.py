from fastapi import APIRouter
from app.models import UserPreferences
from app.services.personalization import save_preferences

router = APIRouter()

# Updates user preferences to make the UX seamless
@router.post("/preferences/{user_id}")
async def update_preferences(user_id: str, payload: UserPreferences):
    await save_preferences(user_id, payload.model_dump())
    return {"message": "Preferences saved"}