# app/main.py
"""
Main FastAPI application entry-point.

• Exposes a module-level `app` object for Uvicorn.
• Creates DB tables on startup (demo-friendly).
• Seeds a default admin user if none exist.
• Mounts all API routers under the versioned prefix.
"""

from fastapi import FastAPI
from sqlmodel import SQLModel, Session, select

from app.core.config import settings
from app.db.session import engine
from app.api.v1.endpoints import auth, devices, users, ingest
from app.models.user import User
from app.utils.security import hash_password


def create_app() -> FastAPI:
    """Build and return a configured FastAPI instance."""
    application = FastAPI(
        title="Cloud Micro-service",
        version="0.1.0",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs",
    )

    # ─────────────────── Startup tasks ──────────────────── #
    @application.on_event("startup")
    def _startup() -> None:
        # 1) Create tables (idempotent)
        SQLModel.metadata.create_all(engine)

        # 2) Seed one admin user if table is empty
        with Session(engine) as session:
            user_exists = session.exec(select(User)).first()
            if not user_exists:
                admin = User(
                    username="admin",
                    email="admin@example.com",
                    hashed_password=hash_password("admin123"),
                )
                session.add(admin)
                session.commit()

    # ─────────────────── Health check ───────────────────── #
    @application.get(f"{settings.API_PREFIX}/health", tags=["health"])
    async def health_check():
        return {"status": "ok"}

    # ─────────────────── Routers ────────────────────────── #
    application.include_router(
        auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["auth"]
    )
    application.include_router(
        users.router, prefix=f"{settings.API_PREFIX}/users", tags=["users"]
    )
    application.include_router(
        devices.router, prefix=f"{settings.API_PREFIX}/devices", tags=["devices"]
    )
    application.include_router(
        ingest.router, prefix=f"{settings.API_PREFIX}", tags=["ingest"]
    )

    return application


# Uvicorn imports `app.main` and looks for this variable:
app: FastAPI = create_app()
