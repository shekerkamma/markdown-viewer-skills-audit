from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.webhooks import router as webhooks_router
from app.config import settings

app = FastAPI(
    title="TicketForge",
    description="From GitHub Issue to merged PR via multi-agent AI pipeline",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.app_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(webhooks_router)
app.include_router(dashboard_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
