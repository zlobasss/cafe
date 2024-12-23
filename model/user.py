# model/user.py
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from model import Base

class Role(PyEnum):
    ADMIN = "Администратор"
    WAITER = "Официант"
    COOK = "Повар"

    @staticmethod
    def get_name_from_value(value):
        return next((role.name for role in Role if role.value == value), None)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    is_active = Column(Boolean, default=True)
    contact_details = Column(String)
    photo_path = Column(String)
    contract_path = Column(String)

    shifts = relationship('Shift', back_populates='admin')
    shift_employees = relationship('ShiftEmployee', back_populates='user')
