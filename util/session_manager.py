# util/session_manager.py
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super_secret_key_123"

class SessionManager:
    """Менеджер сессий для работы с токенами"""

    @staticmethod
    def generate_token(user_id: int) -> str:
        """Генерирует JWT токен для пользователя"""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=2),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_token(token: str) -> dict:
        """Проверяет токен и возвращает полезную нагрузку"""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Срок действия токена истек")
        except jwt.InvalidTokenError:
            raise ValueError("Невалидный токен")

    @staticmethod
    def get_token_from_file() -> str:
        """Получение токена из файла или другого хранилища"""
        try:
            with open("session.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

    @staticmethod
    def save_token_to_file(token: str):
        """Сохранение токена в файл"""
        with open("session.txt", "w") as file:
            file.write(token)

    @staticmethod
    def clear_session():
        """Очистка токена из сессии (удаление файла с токеном)"""
        try:
            # Удаляем файл с токеном, который хранит сессию
            with open("session.txt", "w") as file:
                file.truncate(0)  # Очищаем содержимое файла
        except FileNotFoundError:
            pass  # Если файл не найден, просто игнорируем ошибку
