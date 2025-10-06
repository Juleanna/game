from sqlalchemy import Column, Integer, String, Float, Boolean, Enum as SQLEnum
from app.core.database import Base
import enum


class ItemType(str, enum.Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    QUEST = "quest"
    RESOURCE = "resource"


class ItemRarity(str, enum.Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String)
    item_type = Column(SQLEnum(ItemType), nullable=False)
    rarity = Column(SQLEnum(ItemRarity), default=ItemRarity.COMMON)

    # Базовые характеристики
    weight = Column(Float, default=0.0)
    value = Column(Integer, default=0)  # Цена в золоте
    max_stack = Column(Integer, default=1)  # Максимальное количество в стаке

    # Эффекты предмета
    damage = Column(Integer, default=0)  # Для оружия
    defense = Column(Integer, default=0)  # Для брони
    health_restore = Column(Integer, default=0)  # Для расходников

    # Требования
    required_level = Column(Integer, default=1)
    required_strength = Column(Integer, default=0)
    required_dexterity = Column(Integer, default=0)
    required_intelligence = Column(Integer, default=0)
    required_endurance = Column(Integer, default=0)

    # Флаги
    is_tradeable = Column(Boolean, default=True)
    is_droppable = Column(Boolean, default=True)
    is_questitem = Column(Boolean, default=False)
