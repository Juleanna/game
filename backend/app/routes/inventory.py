from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from ..core.database import get_db
from ..core.dependencies import get_current_active_user
from ..models.user import User
from ..models.character import Character
from ..models.inventory import InventorySlot
from ..models.item import Item

router = APIRouter(prefix="/inventory", tags=["inventory"])


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    item_type: str
    rarity: str
    level_required: int
    strength_bonus: int
    dexterity_bonus: int
    intelligence_bonus: int
    endurance_bonus: int
    damage: int
    defense: int
    value: int

    class Config:
        from_attributes = True


class InventorySlotResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    slot_position: int
    is_equipped: bool
    item: ItemResponse

    class Config:
        from_attributes = True


class EquipItemRequest(BaseModel):
    slot_id: int
    equip: bool  # True - экипировать, False - снять


class MoveItemRequest(BaseModel):
    slot_id: int
    new_position: int


@router.get("/characters/{character_id}", response_model=List[InventorySlotResponse])
async def get_character_inventory(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить инвентарь персонажа"""

    # Проверка прав
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    if character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав доступа")

    # Получаем все слоты инвентаря
    inventory = db.query(InventorySlot).filter(
        InventorySlot.character_id == character_id
    ).order_by(InventorySlot.slot_position).all()

    return inventory


@router.post("/characters/{character_id}/equip")
async def equip_item(
    character_id: int,
    request: EquipItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Экипировать или снять предмет"""

    # Проверка прав
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    if character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав доступа")

    # Находим слот
    slot = db.query(InventorySlot).filter(
        InventorySlot.id == request.slot_id,
        InventorySlot.character_id == character_id
    ).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Слот не найден")

    # Проверяем требования предмета
    item = slot.item
    if request.equip:
        if character.level < item.level_required:
            raise HTTPException(
                status_code=400,
                detail=f"Требуется {item.level_required} уровень"
            )

        # Снимаем другой предмет того же типа
        if item.item_type in ['weapon', 'armor', 'helmet', 'boots', 'gloves']:
            existing_equipped = db.query(InventorySlot).filter(
                InventorySlot.character_id == character_id,
                InventorySlot.is_equipped == True,
                InventorySlot.item_id != slot.item_id
            ).join(Item).filter(
                Item.item_type == item.item_type
            ).first()

            if existing_equipped:
                existing_equipped.is_equipped = False

        slot.is_equipped = True

        # Применяем бонусы
        character.strength += item.strength_bonus
        character.dexterity += item.dexterity_bonus
        character.intelligence += item.intelligence_bonus
        character.endurance += item.endurance_bonus
    else:
        slot.is_equipped = False

        # Убираем бонусы
        character.strength -= item.strength_bonus
        character.dexterity -= item.dexterity_bonus
        character.intelligence -= item.intelligence_bonus
        character.endurance -= item.endurance_bonus

    db.commit()
    db.refresh(slot)

    return {"success": True, "is_equipped": slot.is_equipped}


@router.post("/characters/{character_id}/move")
async def move_item(
    character_id: int,
    request: MoveItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Переместить предмет в другой слот"""

    # Проверка прав
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    if character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав доступа")

    # Находим слот
    slot = db.query(InventorySlot).filter(
        InventorySlot.id == request.slot_id,
        InventorySlot.character_id == character_id
    ).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Слот не найден")

    # Проверяем, не занята ли новая позиция
    existing_slot = db.query(InventorySlot).filter(
        InventorySlot.character_id == character_id,
        InventorySlot.slot_position == request.new_position
    ).first()

    if existing_slot:
        # Меняем местами
        old_position = slot.slot_position
        slot.slot_position = request.new_position
        existing_slot.slot_position = old_position
    else:
        slot.slot_position = request.new_position

    db.commit()

    return {"success": True}


@router.delete("/characters/{character_id}/slots/{slot_id}")
async def delete_item(
    character_id: int,
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удалить предмет из инвентаря"""

    # Проверка прав
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    if character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав доступа")

    # Находим слот
    slot = db.query(InventorySlot).filter(
        InventorySlot.id == slot_id,
        InventorySlot.character_id == character_id
    ).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Слот не найден")

    # Если экипирован, снимаем бонусы
    if slot.is_equipped:
        item = slot.item
        character.strength -= item.strength_bonus
        character.dexterity -= item.dexterity_bonus
        character.intelligence -= item.intelligence_bonus
        character.endurance -= item.endurance_bonus

    db.delete(slot)
    db.commit()

    return {"success": True}
