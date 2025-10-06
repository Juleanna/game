from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class QuestStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Требования
    required_level = Column(Integer, default=1)

    # Награды
    experience_reward = Column(Integer, default=100)
    gold_reward = Column(Integer, default=50)

    # NPC, который выдаёт квест
    npc_id = Column(Integer, ForeignKey("npcs.id"), nullable=True)

    # Цели квеста
    target_monster_id = Column(Integer, ForeignKey("monsters.id"), nullable=True)
    target_kill_count = Column(Integer, default=1)

    # Связи
    npc = relationship("NPC")


class QuestProgress(Base):
    __tablename__ = "quest_progress"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    status = Column(SQLEnum(QuestStatus), default=QuestStatus.NOT_STARTED)

    # Прогресс
    current_progress = Column(Integer, default=0)  # Например, убито монстров

    # Связи
    character = relationship("Character")
    quest = relationship("Quest")
