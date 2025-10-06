from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class InventorySlot(Base):
    __tablename__ = "inventory_slots"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1)
    slot_position = Column(Integer, nullable=False)  # Позиция в инвентаре
    is_equipped = Column(Boolean, default=False)  # Экипирован ли предмет

    # Relationships
    character = relationship("Character", back_populates="inventory")
    item = relationship("Item")
