# app/db/session.py
"""
Database session management.

• Creates async database engine with connection pooling.
• Provides session factory for dependency injection.
• Handles database URL configuration and connection setup.
"""

from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Create async engine for PostgreSQL (with fallback)
try:
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_pre_ping=True,
        pool_recycle=300,
    )
    
    # Create sync engine for migrations and startup tasks
    sync_engine = create_engine(
        settings.DATABASE_URL.replace("+asyncpg", ""),
        echo=settings.DATABASE_ECHO,
    )
except ImportError:
    # Fallback for development without asyncpg
    engine = None
    sync_engine = None

# Session factory for dependency injection
if engine is not None:
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
else:
    AsyncSessionLocal = None


async def get_session() -> AsyncSession:
    """Dependency to get database session."""
    if AsyncSessionLocal is None:
        raise RuntimeError("Database not configured")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()