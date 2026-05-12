from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.auth.security import verify_google_token
from app.auth.recaptcha import verify_captcha

router = APIRouter()

class GoogleAuthRequest(BaseModel):
    token: str

@router.post("/signup")
async def signup(payload: dict):
    valid = await verify_captcha(payload["captcha"])
    if not valid:
        raise HTTPException(400, "Bot detected"
        )
    return {"message": "Human"}

@router.post("/google-login")
async def google_login(payload: GoogleAuthRequest):
    user = verify_google_token(payload.token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    return {
        "message": "Authenticated",
        "user": user
    }