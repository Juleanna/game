"""Сервис для боевой системы"""
import random
from typing import Dict, Tuple


class CombatService:
    """Управление боевыми механиками"""

    @staticmethod
    def calculate_damage(
        attacker_strength: int,
        attacker_level: int,
        defender_defense: int,
        weapon_damage: int = 0,
    ) -> int:
        """
        Расчёт урона от атаки

        Args:
            attacker_strength: Сила атакующего
            attacker_level: Уровень атакующего
            defender_defense: Защита защищающегося
            weapon_damage: Урон от оружия

        Returns:
            Итоговый урон
        """
        # Базовый урон
        base_damage = attacker_strength + weapon_damage + (attacker_level * 2)

        # Критический удар (10% шанс)
        is_critical = random.random() < 0.1
        if is_critical:
            base_damage = int(base_damage * 1.5)

        # Защита уменьшает урон
        final_damage = max(1, base_damage - defender_defense)

        return final_damage

    @staticmethod
    def calculate_exp_reward(monster_level: int, base_exp: int) -> int:
        """Расчёт награды опыта за победу над монстром"""
        return base_exp + (monster_level * 10)

    @staticmethod
    def calculate_level_up(current_exp: int, current_level: int) -> Tuple[bool, int]:
        """
        Проверка, достаточно ли опыта для повышения уровня

        Args:
            current_exp: Текущий опыт
            current_level: Текущий уровень

        Returns:
            Tuple (нужно повысить уровень?, новый уровень)
        """
        exp_needed = current_level * 100  # Формула: 100 опыта на уровень * уровень
        if current_exp >= exp_needed:
            return True, current_level + 1
        return False, current_level

    @staticmethod
    def apply_level_up_bonuses(character) -> Dict[str, int]:
        """
        Применить бонусы при повышении уровня

        Returns:
            Словарь с бонусами
        """
        bonuses = {
            "strength": 2,
            "dexterity": 2,
            "intelligence": 2,
            "endurance": 2,
            "max_health": 20,
        }

        character.strength += bonuses["strength"]
        character.dexterity += bonuses["dexterity"]
        character.intelligence += bonuses["intelligence"]
        character.endurance += bonuses["endurance"]
        character.max_health += bonuses["max_health"]
        character.health = character.max_health  # Полное восстановление

        return bonuses

    @staticmethod
    def monster_ai_attack(monster, character) -> Dict:
        """
        ИИ монстра для атаки персонажа

        Returns:
            Результат атаки
        """
        damage = CombatService.calculate_damage(
            attacker_strength=monster.damage,
            attacker_level=monster.level,
            defender_defense=character.endurance,
            weapon_damage=0,
        )

        character.health = max(0, character.health - damage)

        return {
            "attacker": monster.name,
            "defender": character.name,
            "damage": damage,
            "defender_health": character.health,
            "defender_alive": character.health > 0,
        }


combat_service = CombatService()
