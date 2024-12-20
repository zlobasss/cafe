# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from model import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum('Администратор', 'Официант', 'Повар', name='role_enum'), nullable=False)
    is_active = Column(Boolean, default=True)
    contact_details = Column(String)
    photo_path = Column(String)
    contract_path = Column(String)