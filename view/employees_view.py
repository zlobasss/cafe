#view/employees_view.py

from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from view.employee_list import EmployeeList
from view.employee_form import EmployeeForm
from view.employee_card import EmployeeCard

class EmployeesView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Сотрудники")

        # Основной лэйаут
        self.layout = QVBoxLayout()
        
        # Стек для переключения между представлениями
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)
        
        # Создаем компоненты
        self.employee_list = EmployeeList(self)  # Передаем self как родительский объект
        self.employee_form = EmployeeForm()

        # Добавляем их в стек
        self.stacked_widget.addWidget(self.employee_list)
        self.stacked_widget.addWidget(self.employee_form)

        # Подключаем сигналы для переключения форм
        self.employee_list.switch_to_form_signal.connect(self.show_employee_form)
        self.employee_list.switch_to_card_signal.connect(self.show_employee_card)
        self.employee_form.switch_to_list_signal.connect(self.show_employee_list)

        self.setLayout(self.layout)

    def show_employee_form(self):
        """Показывает форму добавления сотрудника"""
        self.stacked_widget.setCurrentWidget(self.employee_form)

    def show_employee_card(self, user):
        """Показывает карточку сотрудника"""
        self.employee_card = EmployeeCard(user)
        self.employee_card.switch_to_list_signal.connect(self.show_employee_list)
        self.stacked_widget.addWidget(self.employee_card)  # Добавляем карточку в стек
        self.stacked_widget.setCurrentWidget(self.employee_card)  # Переключаемся на карточку

    def show_employee_list(self):
        """Показывает форму добавления сотрудника"""
        self.employee_list.load_users()
        self.stacked_widget.setCurrentWidget(self.employee_list)
