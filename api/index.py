# Simplified Vercel entry point
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import and create app after path adjustment
def create_app():
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from app.api.routers import auth, users, cars, chat
    from app.core.config import settings
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Car Advisor API - A chat-based car recommendation service",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=600,
    )

    app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
    app.include_router(users.router, prefix="/api/v1", tags=["users"])
    app.include_router(cars.router, prefix="/api/v1", tags=["cars"])
    app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

    @app.get("/")
    async def root():
        return {
            "message": "Car Advisor API",
            "status": "running",
            "version": settings.VERSION
        }

    @app.get("/health")
    async def health():
        return {
            "status": "ok",
            "service": "car-advisor-api",
            "database": "serverless-mode"
        }
    
    return app

# Create the app instance
app = create_app()

# Import mangum after app creation to avoid potential conflicts
from mangum import Mangum

# Create the handler
handler = Mangum(app, lifespan="off")

__all__ = ['handler']