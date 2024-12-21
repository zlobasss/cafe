# model/shift.py
from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from model import Base

class Shift(Base):
    __tablename__ = 'shifts'

    id = Column(Integer, primary_key=True)
    shift_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    admin_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    admin = relationship('User', back_populates='shifts')
    employees = relationship('ShiftEmployee', back_populates='shift')