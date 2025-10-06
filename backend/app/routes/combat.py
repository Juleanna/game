from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.character import Character
from app.models.monster import Monster
from app.services.combat_service import combat_service


router = APIRouter(prefix="/combat", tags=["combat"])


class AttackRequest(BaseModel):
    target_monster_id: int


@router.post("/characters/{character_id}/attack")
async def attack_monster(
    character_id: int,
    attack_data: AttackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Атаковать монстра"""

    # Проверка персонажа
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character or character.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    if character.health <= 0:
        raise HTTPException(status_code=400, detail="Персонаж мёртв")

    # Проверка монстра
    monster = (
        db.query(Monster).filter(Monster.id == attack_data.target_monster_id).first()
    )
    if not monster:
        raise HTTPException(status_code=404, detail="Монстр не найден")

    if monster.health <= 0:
        raise HTTPException(status_code=400, detail="Монстр уже мёртв")

    # Расчёт урона от игрока
    player_damage = combat_service.calculate_damage(
        attacker_strength=character.strength,
        attacker_level=character.level,
        defender_defense=monster.defense,
        weapon_damage=0,  # TODO: учитывать оружие из инвентаря
    )

    monster.health = max(0, monster.health - player_damage)

    # Результат атаки игрока
    result = {
        "player_attack": {
            "damage": player_damage,
            "monster_health": monster.health,
            "monster_alive": monster.health > 0,
        }
    }

    # Если монстр жив - он отвечает
    if monster.health > 0:
        counter_attack = combat_service.monster_ai_attack(monster, character)
        result["monster_counter_attack"] = counter_attack
    else:
        # Монстр убит - выдать награды
        exp_reward = combat_service.calculate_exp_reward(
            monster.level, monster.experience_reward
        )
        character.experience += exp_reward
        character.gold += monster.gold_reward

        result["rewards"] = {
            "experience": exp_reward,
            "gold": monster.gold_reward,
        }

        # Проверка повышения уровня
        level_up, new_level = combat_service.calculate_level_up(
            character.experience, character.level
        )
        if level_up:
            character.level = new_level
            bonuses = combat_service.apply_level_up_bonuses(character)
            result["level_up"] = {
                "new_level": new_level,
                "bonuses": bonuses,
            }

        # Удалить мёртвого монстра
        db.delete(monster)

    db.commit()
    db.refresh(character)

    return result


@router.get("/monsters/nearby/{character_id}")
async def get_nearby_monsters(
    character_id: int,
    radius: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Получить список монстров рядом с персонажем"""

    character = db.query(Character).filter(Character.id == character_id).first()
    if not character or character.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Персонаж не найден")

    if not character.location:
        return {"monsters": []}

    # Найти монстров в той же локации
    monsters = (
        db.query(Monster)
        .filter(
            Monster.location_id == character.location_id,
            Monster.health > 0,
        )
        .all()
    )

    return {
        "monsters": [
            {
                "id": m.id,
                "name": m.name,
                "level": m.level,
                "health": m.health,
                "max_health": m.max_health,
                "x": m.x,
                "y": m.y,
                "is_aggressive": m.is_aggressive,
            }
            for m in monsters
        ]
    }
