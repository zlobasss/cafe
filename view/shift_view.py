# view/shift_view.py

from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from view.shift_list import ShiftList
from view.shift_form import ShiftForm
from view.employee_choose import EmployeeChoose

class ShiftView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Смены")

        # Основной лэйаут
        self.layout = QVBoxLayout()

        # Стек для переключения между представлениями
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # Создаем компоненты
        self.shift_list = ShiftList(self)
        self.shift_form = ShiftForm()
        self.employee_choose = EmployeeChoose(self)

        # Добавляем их в стек
        self.stacked_widget.addWidget(self.shift_list)
        self.stacked_widget.addWidget(self.shift_form)
        self.stacked_widget.addWidget(self.employee_choose)

        # Подключаем сигналы для переключения форм
        self.shift_list.switch_to_form_signal.connect(self.show_shift_form)

        # Переключение на список смен после добавления
        self.shift_form.switch_to_list_signal.connect(self.show_shift_list)
        
        self.shift_form.switch_to_choose_signal.connect(self.show_employee_choose)

        self.employee_choose.employee_selected_signal.connect(self.add_employee_to_form)

        self.setLayout(self.layout)

    def add_employee_to_form(self, user):
        self.shift_form.add_employee_to_shift(user)
        self.show_shift_form()

    def show_shift_form(self):
        """Показывает форму добавления смены"""
        self.stacked_widget.setCurrentWidget(self.shift_form)

    def show_shift_list(self):
        """Показывает список смен"""
        self.shift_list.load_shifts()
        self.stacked_widget.setCurrentWidget(self.shift_list)

    def show_employee_choose(self):
        self.stacked_widget.setCurrentWidget(self.employee_choose)
