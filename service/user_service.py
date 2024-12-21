import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from model.user import User
from sqlalchemy.orm import Session
from database import Database

db = Database.get_session()
SECRET_KEY = "super_secret_key_123"

class UserService:

    @staticmethod
    def generate_token(user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),  # Время жизни токена
            "iat": datetime.datetime.utcnow(),  # Время создания токена
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def get_session_user():
        try:
            with open("session.txt", "r") as file:
                token = file.read()
            payload = UserService.verify_token(token)
            user_id = payload["user_id"]
            user = UserService.get_user_by_id(user_id)
            return user
        except (FileNotFoundError, ValueError) as e:
            print(f"Ошибка при получении пользователя: {str(e)}")
            return None

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Срок действия токена истек")
        except jwt.InvalidTokenError:
            raise ValueError("Невалидный токен")

    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password)

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        print(generate_password_hash("QWEasd123!", "scrypt"))
        return check_password_hash(stored_password, provided_password)

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
    def get_users_with_pagination(page: int, page_size: int) -> dict:
        total_users = db.query(User).count()
        total_pages = (total_users + page_size - 1) // page_size  # Округление вверх

        if page < 1 or page > total_pages:
            return {
                "users": [],
                "total_users": total_users,
                "total_pages": total_pages,
                "current_page": page,
            }

        offset = (page - 1) * page_size
        users = db.query(User).offset(offset).limit(page_size).all()

        return {
            "users": users,
            "total_users": total_users,
            "total_pages": total_pages,
            "current_page": page,
        }

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
    def find_by_username(username: str) -> User:
        return db.query(User).filter(User.username == username).first()
