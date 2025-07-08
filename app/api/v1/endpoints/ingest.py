# app/api/v1/endpoints/ingest.py
"""
Data ingestion endpoints.

• Receive sensor data from IoT devices.
• Store sensor readings in database.
• Validate and process incoming data.
"""

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.models.sensor import Sensor
from app.models.device import Device

router = APIRouter()


@router.post("/ingest")
async def ingest_sensor_data(
    device_id: str,
    sensor_type: str,
    value: float,
    unit: str = "",
    metadata: str = None,
    session: AsyncSession = Depends(get_session)
) -> Any:
    """Ingest sensor data from IoT devices."""
    from sqlmodel import select
    from uuid import UUID
    
    try:
        device_uuid = UUID(device_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid device ID format"
        )
    
    # Verify device exists and is active
    result = await session.exec(select(Device).where(Device.id == device_uuid))
    device = result.first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    if not device.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device is not active"
        )
    
    # Create sensor reading
    sensor = Sensor(
        device_id=device_uuid,
        sensor_type=sensor_type,
        value=value,
        unit=unit,
        sensor_metadata=metadata
    )
    
    session.add(sensor)
    await session.commit()
    await session.refresh(sensor)
    
    return {
        "id": str(sensor.id),
        "device_id": str(sensor.device_id),
        "sensor_type": sensor.sensor_type,
        "value": sensor.value,
        "unit": sensor.unit,
        "timestamp": sensor.timestamp
    }


@router.get("/sensors/{device_id}")
async def get_device_sensors(
    device_id: str,
    sensor_type: str = None,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
) -> Any:
    """Get sensor readings for a specific device."""
    from sqlmodel import select
    from uuid import UUID
    
    try:
        device_uuid = UUID(device_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid device ID format"
        )
    
    # Build query
    query = select(Sensor).where(Sensor.device_id == device_uuid)
    if sensor_type:
        query = query.where(Sensor.sensor_type == sensor_type)
    
    query = query.order_by(Sensor.timestamp.desc()).limit(limit)
    
    result = await session.exec(query)
    sensors = result.all()
    
    return [
        {
            "id": str(sensor.id),
            "sensor_type": sensor.sensor_type,
            "value": sensor.value,
            "unit": sensor.unit,
            "timestamp": sensor.timestamp,
            "metadata": sensor.sensor_metadata
        }
        for sensor in sensors
    ]