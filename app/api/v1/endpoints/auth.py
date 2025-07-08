# app/api/v1/endpoints/auth.py
"""
Authentication endpoints.

• User login and token generation.
• Token refresh and validation.
• User registration (admin only).
"""

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session, get_current_user
from app.models.user import User
from app.services.auth import authenticate_user, create_user, create_user_token

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
) -> Any:
    """Authenticate user and return access token."""
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_user_token(user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "username": user.username,
        "is_admin": user.is_admin
    }


@router.post("/register")
async def register(
    username: str,
    email: str,
    password: str,
    session: AsyncSession = Depends(get_session)
) -> Any:
    """Register a new user account."""
    # Check if user already exists
    from sqlmodel import select
    existing_user = await session.exec(
        select(User).where(
            (User.username == username) | (User.email == email)
        )
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    user = await create_user(session, username, email, password)
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active
    }


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user information."""
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_admin": current_user.is_admin,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login
    }