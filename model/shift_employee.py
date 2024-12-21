# model/shift_employee.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from model import Base

class ShiftEmployee(Base):
    __tablename__ = 'shift_employees'

    shift_id = Column(Integer, ForeignKey('shifts.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    shift = relationship('Shift', back_populates='employees')
    user = relationship('User', back_populates='shift_employees')