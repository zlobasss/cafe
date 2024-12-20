# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User

# Настройки базы данных
engine = create_engine("sqlite:///cafe.db")
Session = sessionmaker(bind=engine)

class Database:
    @staticmethod
    def get_session():
        return Session()

    @staticmethod
    def create_tables():
        Base.metadata.create_all(engine)
