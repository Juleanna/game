from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class NPCType(str, enum.Enum):
    TRADER = "trader"
    QUEST_GIVER = "quest_giver"
    GUARD = "guard"
    NEUTRAL = "neutral"


class NPC(Base):
    __tablename__ = "npcs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    npc_type = Column(SQLEnum(NPCType), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    # Характеристики
    level = Column(Integer, default=1)
    health = Column(Integer, default=100)
    max_health = Column(Integer, default=100)

    # Торговля (для торговцев)
    is_trader = Column(Boolean, default=False)
    gold = Column(Integer, default=1000)

    # Диалог
    dialogue = Column(String, default="Привет, путник!")

    # Связи
    location = relationship("Location")
