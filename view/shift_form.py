# view/shift_form.py

from PyQt5.QtWidgets import QMessageBox, QAbstractItemView, QHeaderView, QHBoxLayout, QTableWidgetItem, QVBoxLayout, QFormLayout, QLabel, QDateEdit, QTimeEdit, QPushButton, QTableWidget, QWidget
from PyQt5.QtCore import pyqtSignal, Qt, QDate, QTime
from service.shift_service import ShiftService
from service.user_service import UserService
from view.employee_choose import EmployeeChoose
from datetime import datetime

class ShiftForm(QWidget):
    switch_to_list_signal = pyqtSignal()
    switch_to_choose_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Создать смену")
        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.employees_id = []

        # Поля формы
        self.date_input = QDateEdit(self)
        self.date_input.setDate(QDate.currentDate().addDays(1))
        self.form_layout.addRow(QLabel("Дата:"), self.date_input)

        self.time_start_input = QTimeEdit(self)
        self.time_start_input.setTime(QTime(8, 0, 0, 0))
        self.form_layout.addRow(QLabel("Время начала:"), self.time_start_input)

        self.time_end_input = QTimeEdit(self)
        self.time_end_input.setTime(QTime(22, 0, 0, 0))
        self.form_layout.addRow(QLabel("Время конца:"), self.time_end_input)

        # Кнопка добавления сотрудника на смену
        self.add_employee = QPushButton("Добавить сотрудника", self)
        self.add_employee.clicked.connect(self.choose_employee_to_shift)
        self.form_layout.addWidget(self.add_employee)

        # Таблица сотрудников
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)  # Фамилия, Имя, Отчество, Роль
        self.table_widget.setHorizontalHeaderLabels(
            ["Фамилия", "Имя", "Отчество", "Роль"]
        )

        # Запрещаем редактирование таблицы
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Настройка растягивания столбцов
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.form_layout.addRow(QLabel("Сотрудники:"), self.table_widget)

        self.buttons = QHBoxLayout()

        # Кнопка отмены
        self.cancel_button = QPushButton("Отмена", self)
        self.cancel_button.setObjectName("cancel_button")  # Устанавливаем имя объекта для применения стиля
        self.cancel_button.clicked.connect(self.cancel_shift)
        self.buttons.addWidget(self.cancel_button)


        self.empty_label = QLabel("")
        self.buttons.addWidget(self.empty_label)

        # Кнопка сохранения
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.setObjectName("save_button")  # Устанавливаем имя объекта для применения стиля
        self.save_button.clicked.connect(self.save_shift)
        self.buttons.addWidget(self.save_button)


        self.layout.addLayout(self.buttons)
        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout)

        # Подключаем обработку двойного клика по строке таблицы
        self.table_widget.doubleClicked.connect(self.remove_employee_on_double_click)

    def save_shift(self):
        # Преобразование даты и времени
        date_str = self.date_input.date().toString("yyyy-MM-dd")
        start_time_str = self.time_start_input.time().toString("HH:mm")
        end_time_str = self.time_end_input.time().toString("HH:mm")

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()

        # Валидация данных формы
        if len(self.employees_id) < 4 or len(self.employees_id) > 7:
            QMessageBox.warning(self, "Ошибка", "Количество сотрудников должно быть от 4 до 7.")
            return

        if start_time >= end_time:
            QMessageBox.warning(self, "Ошибка", "Время начала должно быть раньше времени конца.")
            return

        responsible = UserService.get_session_user().id

        try:
            shift = ShiftService.create_shift(date, start_time, end_time, responsible, self.employees_id)
            QMessageBox.information(self, "Успех", "Смена успешно создана!")
            self.switch_to_list_signal.emit()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать смену: {str(e)}")

    def choose_employee_to_shift(self):
        self.switch_to_choose_signal.emit()

    def add_employee_to_shift(self, user):
        if len(self.employees_id) >= 7:
            QMessageBox.warning(self, "Ошибка", "Максимальное количество сотрудников в смене — 7.")
            return

        if user.id not in self.employees_id:  # Проверка на уникальность сотрудника
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(user.last_name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(user.first_name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(user.second_name))
            self.table_widget.setItem(row, 3, QTableWidgetItem(user.role.value))
            self.employees_id.append(user.id)
        else:
            QMessageBox.warning(self, "Ошибка", "Этот сотрудник уже добавлен.")

    def remove_employee_on_double_click(self, index):
        row = index.row()
        employee_id = self.employees_id[row]

        # Удаляем из таблицы
        self.table_widget.removeRow(row)
        # Удаляем из списка сотрудников
        self.employees_id.remove(employee_id)

        QMessageBox.information(self, "Успех", f"Сотрудник удален из смены.")

    def cancel_shift(self):
        # Сбрасываем данные формы
        self.date_input.setDate(QDate.currentDate().addDays(1))
        self.time_start_input.setTime(QTime(8, 0, 0, 0))
        self.time_end_input.setTime(QTime(22, 0, 0, 0))
        self.employees_id.clear()
        self.table_widget.setRowCount(0)
        self.switch_to_list_signal.emit()
