# service/user_service.py

from werkzeug.security import generate_password_hash, check_password_hash
from model.user import User
from sqlalchemy.orm import Session
from database import Database
from util.session_manager import SessionManager  # Импорт менеджера сессий для работы с токенами

db = Database.get_session()
SECRET_KEY = "super_secret_key_123"

class UserService:
    """Сервис для работы с пользователями"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширует пароль перед сохранением в базу данных."""
        return generate_password_hash(password)

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """Проверяет пароль пользователя."""
        return check_password_hash(stored_password, provided_password)

    @staticmethod
    def create_user(new_user: User) -> User:
        """Создает нового пользователя."""
        new_user.password = UserService.hash_password(new_user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """Получает пользователя по ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users() -> list[User]:
        """Получает всех пользователей."""
        return db.query(User).all()

    @staticmethod
    def get_users_with_pagination(page: int, page_size: int) -> dict:
        """Получает список пользователей с пагинацией."""
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
        """Обновляет данные пользователя."""
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
        """Удаляет пользователя."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True

    @staticmethod
    def find_by_username(username: str) -> User:
        """Ищет пользователя по имени пользователя."""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def generate_token(user_id: int) -> str:
        """Генерирует JWT токен для пользователя."""
        return SessionManager.generate_token(user_id)

    @staticmethod
    def get_session_user() -> User:
        """Получает текущего пользователя по токену из сессии."""
        try:
            token = SessionManager.get_token_from_file()  # Метод для получения токена из файла
            if token:
                payload = SessionManager.verify_token(token)  # Проверка токена
                user_id = payload["user_id"]
                return UserService.get_user_by_id(user_id)
        except (FileNotFoundError, ValueError) as e:
            print(f"Ошибка при получении пользователя: {str(e)}")
            return None

    @staticmethod
    def clear_session():
        """Очищает сессию пользователя."""
        SessionManager.clear_session()
