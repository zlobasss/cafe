from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from service.user_service import UserService

class EmployeeCard(QWidget):

    switch_to_list_signal = pyqtSignal()
    employee = None

    def __init__(self, employee: object, parent=None):
        super().__init__(parent)
        self.employee = employee

        self.setWindowTitle(f"Карточка сотрудника: {employee.first_name} {employee.last_name}")
        self.layout = QVBoxLayout()

        # Поля карточки
        self.layout.addWidget(QLabel(f"Фамилия: {employee.last_name}"))
        self.layout.addWidget(QLabel(f"Имя: {employee.first_name}"))
        self.layout.addWidget(QLabel(f"Отчество: {employee.second_name}"))
        self.layout.addWidget(QLabel(f"Роль: {employee.role}"))
        self.layout.addWidget(QLabel(f"Контакты: {employee.contact_details}"))
        self.layout.addWidget(QLabel(f"Статус: {'Активен' if employee.is_active else 'Уволен'}"))
        self.layout.addWidget(QLabel(f"Фото: {employee.photo_path}"))
        self.layout.addWidget(QLabel(f"Контракт: {employee.contract_path}"))

        # Создаем горизонтальный контейнер для кнопок
        button_layout = QHBoxLayout()

        # Кнопка "Уволить"
        self.terminate_button = QPushButton("Уволить", self)
        self.terminate_button.clicked.connect(self.terminate_employee)  # Функция увольнения
        button_layout.addWidget(self.terminate_button)

        # Добавляем пустое пространство между кнопками
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer)

        # Кнопка "Закрыть"
        self.close_button = QPushButton("Закрыть", self)
        self.close_button.clicked.connect(self.open_employee_list)
        button_layout.addWidget(self.close_button)

        # Добавляем горизонтальный контейнер с кнопками в основной лэйаут
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def terminate_employee(self):
        if self.employee:
            self.employee.is_active = False  # Изменение статуса сотрудника на "неактивен"
            UserService.update_user(self.employee)  # Обновляем данные сотрудника в базе данных
            self.open_employee_list()
            QMessageBox.information(self, "Успех", f"Сотрудник {self.employee.first_name} {self.employee.last_name} уволен.")

    def open_employee_list(self):
        self.switch_to_list_signal.emit()
