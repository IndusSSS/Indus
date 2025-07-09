# app/api/v1/endpoints/devices.py
"""
Device management endpoints.

• CRUD operations for IoT devices.
• Device status monitoring.
• Device registration and configuration.
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session, get_current_active_user
from app.models.device import Device
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_devices(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get list of devices."""
    from sqlmodel import select
    result = await session.exec(select(Device).offset(skip).limit(limit))
    devices = result.all()
    
    return [
        {
            "id": str(device.id),
            "name": device.name,
            "description": device.description,
            "is_active": device.is_active
        }
        for device in devices
    ]


@router.post("/")
async def create_device(
    name: str,
    description: str = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create a new device."""
    device = Device(
        name=name,
        description=description
    )
    session.add(device)
    await session.commit()
    await session.refresh(device)
    
    return {
        "id": str(device.id),
        "name": device.name,
        "description": device.description,
        "is_active": device.is_active
    }


@router.get("/{device_id}")
async def get_device(
    device_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get device by ID."""
    from sqlmodel import select
    from uuid import UUID
    
    try:
        device_uuid = UUID(device_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid device ID format"
        )
    
    result = await session.exec(select(Device).where(Device.id == device_uuid))
    device = result.first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    return {
        "id": str(device.id),
        "name": device.name,
        "description": device.description,
        "is_active": device.is_active
    }


@router.put("/{device_id}")
async def update_device(
    device_id: str,
    name: str = None,
    description: str = None,
    is_active: bool = None,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Update device information."""
    from sqlmodel import select
    from uuid import UUID
    
    try:
        device_uuid = UUID(device_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid device ID format"
        )
    
    result = await session.exec(select(Device).where(Device.id == device_uuid))
    device = result.first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    if name is not None:
        device.name = name
    if description is not None:
        device.description = description
    if is_active is not None:
        device.is_active = is_active
    
    session.add(device)
    await session.commit()
    await session.refresh(device)
    
    return {
        "id": str(device.id),
        "name": device.name,
        "description": device.description,
        "is_active": device.is_active
    }