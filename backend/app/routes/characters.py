from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from ..core.database import get_db
from ..core.dependencies import get_current_active_user
from ..models.user import User
from ..models.character import Character, ProfessionType, GenderType

router = APIRouter(prefix="/characters", tags=["characters"])


class CharacterCreate(BaseModel):
    name: str
    profession: ProfessionType
    gender: GenderType


class CharacterResponse(BaseModel):
    id: int
    name: str
    profession: str
    gender: str
    level: int
    health: int
    max_health: int
    strength: int
    dexterity: int
    intelligence: int
    endurance: int
    experience: int
    gold: int
    location_id: int | None

    class Config:
        from_attributes = True


@router.post("/", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
async def create_character(
    character_data: CharacterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Создание нового персонажа"""

    # Проверка уникальности имени
    existing_character = db.query(Character).filter(
        Character.name == character_data.name
    ).first()

    if existing_character:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Персонаж с таким именем уже существует"
        )

    # Ограничение на количество персонажей (например, максимум 3)
    user_characters_count = db.query(Character).filter(
        Character.user_id == current_user.id
    ).count()

    if user_characters_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Достигнут лимит персонажей (максимум 3)"
        )

    # Бонусы характеристик в зависимости от профессии
    stat_bonuses = {
        ProfessionType.MERCENARY: {"strength": 5, "endurance": 3},
        ProfessionType.STALKER: {"dexterity": 5, "endurance": 2},
        ProfessionType.PSIONIC: {"intelligence": 5, "endurance": 2},
        ProfessionType.ENGINEER: {"intelligence": 4, "dexterity": 3},
        ProfessionType.MEDIC: {"intelligence": 4, "endurance": 3},
        ProfessionType.SCOUT: {"dexterity": 4, "intelligence": 3},
        ProfessionType.SCIENTIST: {"intelligence": 5, "strength": 2},
        ProfessionType.HUNTER: {"dexterity": 4, "strength": 3},
        ProfessionType.GUARD: {"strength": 4, "endurance": 3},
        ProfessionType.MECHANIC: {"intelligence": 3, "dexterity": 4},
        ProfessionType.SMUGGLER: {"dexterity": 4, "intelligence": 3},
        ProfessionType.CORSAIR: {"dexterity": 3, "strength": 4},
        ProfessionType.JOURNALIST: {"intelligence": 4, "dexterity": 3},
        ProfessionType.TRADER: {"intelligence": 3, "dexterity": 4},
    }

    # Базовые характеристики
    base_stats = {
        "strength": 10,
        "dexterity": 10,
        "intelligence": 10,
        "endurance": 10
    }

    # Применение бонусов профессии
    bonuses = stat_bonuses.get(character_data.profession, {})
    for stat, bonus in bonuses.items():
        base_stats[stat] += bonus

    # Создание персонажа
    character = Character(
        user_id=current_user.id,
        name=character_data.name,
        profession=character_data.profession,
        gender=character_data.gender,
        strength=base_stats["strength"],
        dexterity=base_stats["dexterity"],
        intelligence=base_stats["intelligence"],
        endurance=base_stats["endurance"],
        max_health=100 + base_stats["endurance"] * 5,
        health=100 + base_stats["endurance"] * 5
    )

    db.add(character)
    db.commit()
    db.refresh(character)

    return character


@router.get("/", response_model=List[CharacterResponse])
async def get_user_characters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение всех персонажей текущего пользователя"""

    characters = db.query(Character).filter(
        Character.user_id == current_user.id
    ).all()

    return characters


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение информации о конкретном персонаже"""

    character = db.query(Character).filter(
        Character.id == character_id,
        Character.user_id == current_user.id
    ).first()

    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Персонаж не найден"
        )

    return character


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удаление персонажа"""

    character = db.query(Character).filter(
        Character.id == character_id,
        Character.user_id == current_user.id
    ).first()

    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Персонаж не найден"
        )

    db.delete(character)
    db.commit()

    return None
