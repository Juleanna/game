from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.character import Character


router = APIRouter(prefix="/movement", tags=["movement"])


class MoveRequest(BaseModel):
    x: int
    y: int


class MoveRequestWithCharacter(BaseModel):
    character_id: int
    x: int
    y: int


@router.post("/characters/{character_id}/move")
async def move_character(
    character_id: int,
    move_data: MoveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Переместить персонажа на новые координаты"""

    # Проверка существования персонажа
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    # Проверка прав доступа
    if character.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Нет прав для управления этим персонажем"
        )

    # Валидация координат (примерные границы карты)
    if not (0 <= move_data.x <= 1000) or not (0 <= move_data.y <= 1000):
        raise HTTPException(
            status_code=400, detail="Координаты за пределами карты"
        )

    # Обновление позиции персонажа через локацию
    if character.location:
        character.location.x = move_data.x
        character.location.y = move_data.y
    else:
        # Создать начальную локацию, если её нет
        from app.models.location import Location

        location = Location(
            name=f"Position {move_data.x},{move_data.y}",
            description="Temporary location",
            x=move_data.x,
            y=move_data.y,
            radiation_level=0,
            is_safe_zone=False,
            is_city=False
        )
        db.add(location)
        db.commit()
        db.refresh(location)
        character.location_id = location.id

    db.commit()
    db.refresh(character)

    return {
        "success": True,
        "character_id": character.id,
        "x": character.location.x if character.location else move_data.x,
        "y": character.location.y if character.location else move_data.y,
    }


@router.post("/move")
async def move_character_simple(
    move_data: MoveRequestWithCharacter,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Универсальный endpoint для перемещения персонажа (используется для телепортации)"""

    # Проверка существования персонажа
    character = db.query(Character).filter(Character.id == move_data.character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    # Проверка прав доступа
    if character.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Нет прав для управления этим персонажем"
        )

    # Находим локацию на указанных координатах
    from app.models.location import Location

    target_location = db.query(Location).filter(
        Location.x == move_data.x,
        Location.y == move_data.y
    ).first()

    if not target_location:
        raise HTTPException(
            status_code=404,
            detail="Локация не найдена. Используйте только существующие локации из списка."
        )

    # Устанавливаем персонажа в найденную локацию
    character.location_id = target_location.id

    db.commit()
    db.refresh(character)

    return {
        "success": True,
        "character_id": character.id,
        "x": character.location.x if character.location else move_data.x,
        "y": character.location.y if character.location else move_data.y,
        "location_id": character.location_id
    }


@router.get("/characters/{character_id}/position")
async def get_character_position(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Получить текущую позицию персонажа"""

    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    if character.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Нет прав для просмотра этого персонажа"
        )

    if not character.location:
        return {"x": 0, "y": 0, "location_id": None}

    return {
        "x": character.location.x,
        "y": character.location.y,
        "location_id": character.location.id,
    }
