from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check():
    return {"status": "healthy!"}

@router.get("/live")
async def liveness_probe():
    return {"status": "alive"}

@router.get("/ready")
async def readiness_probe():
    return {"status": "ready"}