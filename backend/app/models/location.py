from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base


class Location(Base):
    """Модель локации на карте мира"""

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    x = Column(Integer, nullable=False)  # Координата X
    y = Column(Integer, nullable=False)  # Координата Y

    # Параметры локации
    radiation_level = Column(Integer, default=0)  # Уровень радиации
    is_safe_zone = Column(Boolean, default=False)  # Безопасная зона (нет PvP)
    is_city = Column(Boolean, default=False)  # Город/поселение

    # Tilemap - карта локации в формате JSON
    # Массив 20x15 тайлов, каждый тайл - тип местности
    tilemap = Column(Text, default='[]')  # JSON массив

    # Связи
    characters = relationship("Character", back_populates="location")
