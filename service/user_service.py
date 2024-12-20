# services/user_service.py
import bcrypt
from model.user import User
from sqlalchemy.orm import Session
from database import Database

db = Database.get_session()

class UserService:

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def create_user(new_user: User) -> User:
        new_user.password = UserService.hash_password(new_user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users() -> list[User]:
        return db.query(User).all()

    @staticmethod
    def update_user(user: User) -> User:
        existing_user = db.query(User).filter(User.id == user.id).first()
        if not existing_user:
            return None

        for attr, value in vars(user).items():
            if value is not None and attr != "id":
                setattr(existing_user, attr, value)

        db.commit()
        db.refresh(existing_user)
        return existing_user

    @staticmethod
    def delete_user(user_id: int) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    @staticmethod
    def find_by_username(username: str) -> User:
        return db.query(User).filter(User.username == username).first()
