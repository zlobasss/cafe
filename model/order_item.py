from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from model import Base

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    item_total = Column(Float, nullable=False)

    order = relationship('Order', back_populates='items')
    menu_item = relationship('MenuItem')
