from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class ProfessionType(str, enum.Enum):
    """Профессии персонажей"""
    CORSAIR = "corsair"
    MERCENARY = "mercenary"
    STALKER = "stalker"
    JOURNALIST = "journalist"
    TRADER = "trader"
    PSIONIC = "psionic"
    ENGINEER = "engineer"
    MEDIC = "medic"
    SCOUT = "scout"
    SCIENTIST = "scientist"
    HUNTER = "hunter"
    GUARD = "guard"
    MECHANIC = "mechanic"
    SMUGGLER = "smuggler"


class GenderType(str, enum.Enum):
    """Пол персонажа"""
    male = "male"
    female = "female"
    other = "other"


class Character(Base):
    """Модель персонажа"""

    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    profession = Column(Enum(ProfessionType), nullable=False)
    gender = Column(Enum(GenderType), nullable=False, default=GenderType.male)
    level = Column(Integer, default=1)

    # Характеристики
    health = Column(Integer, default=100)
    max_health = Column(Integer, default=100)
    strength = Column(Integer, default=10)
    dexterity = Column(Integer, default=10)
    intelligence = Column(Integer, default=10)
    endurance = Column(Integer, default=10)

    # Опыт и валюта
    experience = Column(Integer, default=0)
    gold = Column(Integer, default=100)

    # Локация
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

    # Связи
    user = relationship("User", back_populates="characters")
    location = relationship("Location", back_populates="characters")
    inventory = relationship("InventorySlot", back_populates="character", cascade="all, delete-orphan")
