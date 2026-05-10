from app.services.firestore_service import db

async def save_preferences(user_id: str, preferences: dict):
    db.collection("preferences").document(user_id).set(
        preferences
    )

    return True