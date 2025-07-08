# app/models/device.py
from uuid import UUID, uuid4
from typing import Optional

from sqlmodel import SQLModel, Field


class Device(SQLModel, table=True):
    """
    IoT device registry table.

    • `id` – UUID primary-key.
    • `name` – human-friendly label.
    • `description` – optional notes.
    • `is_active` – soft-delete / enable flag.
    """
    __tablename__ = "device"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
