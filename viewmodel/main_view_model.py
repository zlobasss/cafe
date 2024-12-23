# viewmodel/main_view_model.py

from PyQt5.QtCore import QObject, pyqtSignal
from service.user_service import UserService
from view.shift_view import ShiftView
from view.employees_view import EmployeesView
from view.order_view import OrderView
from view.table_view import TableView
from view.menu_item_view import MenuItemView
from model.user import Role


class MainViewModel(QObject):
    # Сигналы для обновления интерфейса
    user_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._user = None
        self._views_cook = [
            ("Заказы", OrderView())
        ]
        self._views_waiter = [
            ("Заказы", OrderView()),
        ]
        self._views_admin = [
            ("Сотрудники", EmployeesView()),
            ("Смены", ShiftView()),
            ("Заказы", OrderView()),
            ("Столы", TableView()),
            ("Позиции", MenuItemView())
        ]
    
    def load_user(self):
        """Загружает пользователя из сессии"""
        self._user = UserService.get_session_user()
        if self._user:
            self.user_updated.emit(f"Приветствую, {self._user.first_name} {self._user.last_name}")
    
    def get_views(self):
        """Возвращает список виджетов"""
        self._user = UserService.get_session_user()
        self._views = []
        if self._user:
            if (self._user.role == Role.ADMIN):
                self._views = self._views_admin
            if (self._user.role == Role.COOK):
                self._views = self._views_cook
            if (self._user.role == Role.WAITER):
                self._views = self._views_waiter
        return self._views
    
    def logout(self):
        """Выход из системы и очистка сессии"""
        UserService.clear_session()  # Создать метод для очистки сессии
        self._user = None
        self.user_updated.emit("Пользователь не авторизован")
