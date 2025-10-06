from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Monster(Base):
    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer, default=1)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    # Характеристики
    health = Column(Integer, default=100)
    max_health = Column(Integer, default=100)
    damage = Column(Integer, default=10)
    defense = Column(Integer, default=5)

    # Награды
    experience_reward = Column(Integer, default=50)
    gold_reward = Column(Integer, default=10)

    # Позиция на карте
    x = Column(Float, default=0.0)
    y = Column(Float, default=0.0)

    # Агрессивность
    is_aggressive = Column(Integer, default=1)  # 1 = агрессивный, 0 = мирный

    # Связи
    location = relationship("Location")
