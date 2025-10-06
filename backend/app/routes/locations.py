from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from ..core.database import get_db
from ..core.dependencies import get_current_active_user
from ..models.user import User
from ..models.location import Location

router = APIRouter(prefix="/locations", tags=["locations"])


class LocationResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    x: int
    y: int
    radiation_level: int
    is_safe_zone: bool
    is_city: bool
    tilemap: str

    class Config:
        from_attributes = True


@router.get("/", response_model=List[LocationResponse])
async def get_all_locations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение всех локаций"""
    locations = db.query(Location).all()
    return locations


@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение информации о конкретной локации"""
    location = db.query(Location).filter(Location.id == location_id).first()

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Локация не найдена"
        )

    return location
