from sqlalchemy import Column, Integer, String
from model import Base

class Table(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
