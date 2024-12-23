from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Float
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from model import Base

class OrderStatus(PyEnum):
    ACCEPTED = 'Принят'
    COOKING = 'Готовится'
    READY = 'Готов'
    PAID = 'Оплачен'

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey('tables.id'), nullable=False)
    waiter_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatus), default=OrderStatus.ACCEPTED)
    total_amount = Column(Float, default=0.0)

    table = relationship('Table')
    waiter = relationship('User')
    shift = relationship('Shift')
    items = relationship('OrderItem', back_populates='order')
