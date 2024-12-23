from sqlalchemy import Column, Integer, String, Boolean, Float
from model import Base

class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    is_available = Column(Boolean, default=True)
