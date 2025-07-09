# app/api/v1/endpoints/users.py
"""
User management endpoints.

• CRUD operations for user accounts.
• User profile management.
• Admin-only user administration.
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session, get_current_active_user, get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """Get list of users (admin only)."""
    from sqlmodel import select
    result = await session.exec(select(User).offset(skip).limit(limit))
    users = result.all()
    
    return [
        {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "created_at": user.created_at
        }
        for user in users
    ]


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get user by ID."""
    from sqlmodel import select
    from uuid import UUID
    
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    result = await session.exec(select(User).where(User.id == user_uuid))
    user = result.first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Users can only see their own profile unless they're admin
    if not current_user.is_admin and current_user.id != user_uuid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "created_at": user.created_at,
        "last_login": user.last_login
    }


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    is_active: bool = None,
    is_admin: bool = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """Update user status (admin only)."""
    from sqlmodel import select
    from uuid import UUID
    
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    result = await session.exec(select(User).where(User.id == user_uuid))
    user = result.first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if is_active is not None:
        user.is_active = is_active
    if is_admin is not None:
        user.is_admin = is_admin
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    return {
        "id": str(user.id),
        "username": user.username,
        "is_active": user.is_active,
        "is_admin": user.is_admin
    }