# viewmodel_login_view_model.py
from service.shift_service import ShiftService

class LoginViewModel:
    """Модель представления для экрана авторизации"""

    def __init__(self, user_service, session_manager):
        self.user_service = user_service
        self.session_manager = session_manager

    def authenticate_user(self, username: str, password: str):
        """Проверяет логин и пароль пользователя."""
        if not username or not password:
            raise ValueError("Заполните все поля!")

        user = self.user_service.find_by_username(username)
        if not user or not self.user_service.verify_password(user.password, password):
            raise ValueError("Неверные данные!")
        
        if not user.is_active:
            raise ValueError("Вы были уволены!")

        token = self.user_service.generate_token(user.id)
        self.session_manager.save_token_to_file(token)
        return "Авторизация успешна!"
    
    def get_user_shifts(self, user):
        if (not user):
            return []
        return ShiftService.get_shifts_by_user_id(user_id=user.id)


    def get_authenticated_user(self):
        """Проверка текущей сессии пользователя."""
        try:
            token = self.session_manager.get_token_from_file()
            if token:
                payload = self.session_manager.verify_token(token)
                return self.user_service.get_user_by_id(payload["user_id"])
        except (FileNotFoundError, ValueError) as e:
            return None
