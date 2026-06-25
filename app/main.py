from fastapi import FastAPI

from app.api.routes.planner import router as planner_router
from app.api.routes.chat import router as chat_router
from app.api.routes.healths import router as health_router
from app.api.routes.admin import router as admin_router

app = FastAPI(title="Waypoint API", version="1.0.0")

app.include_router(planner_router)
app.include_router(chat_router)
app.include_router(health_router)
app.include_router(admin_router)

@app.get("/")
async def root():
    return {"message": "Waypoint API Is Live and Running"}