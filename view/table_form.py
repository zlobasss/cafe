from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QMessageBox
from PyQt5.QtCore import pyqtSignal
from service.table_service import TableService


class TableForm(QWidget):
    switch_to_list_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить стол")
        self.layout = QVBoxLayout()

        # Формат формы
        self.form_layout = QFormLayout()

        # Поля ввода
        self.table_name_input = QLineEdit(self)
        self.form_layout.addRow(QLabel("Название стола:"), self.table_name_input)

        self.capacity_input = QSpinBox(self)
        self.capacity_input.setMinimum(1)
        self.form_layout.addRow(QLabel("Вместимость:"), self.capacity_input)

        self.layout.addLayout(self.form_layout)

        # Кнопки управления
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_table)
        self.layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Отмена", self)
        self.cancel_button.clicked.connect(self.cancel_form)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def save_table(self):
        """Сохраняет новый стол."""
        table_name = self.table_name_input.text().strip()
        capacity = self.capacity_input.value()

        if not table_name or capacity <= 0:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        try:
            TableService.create_table(table_name, capacity)
            QMessageBox.information(self, "Успех", "Стол успешно добавлен!")
            self.switch_to_list_signal.emit()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить стол: {str(e)}")

    def cancel_form(self):
        """Отменяет добавление стола и возвращает к списку."""
        self.clear_form()
        self.switch_to_list_signal.emit()

    def clear_form(self):
        """Очищает данные формы."""
        self.table_name_input.clear()
        self.capacity_input.setValue(1)
