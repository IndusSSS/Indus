# app/models/user.py
"""
User model for authentication and authorization.

• Stores user credentials and profile information.
• Uses Argon2 password hashing for security.
• Supports role-based access control.
"""

from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    User account table.
    
    • `id` – UUID primary key.
    • `username` – unique login identifier.
    • `email` – unique email address.
    • `hashed_password` – Argon2 hashed password.
    • `is_active` – account status flag.
    • `is_admin` – administrative privileges.
    • `created_at` – account creation timestamp.
    """
    __tablename__ = "users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    username: str = Field(unique=True, index=True, nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(default=None)