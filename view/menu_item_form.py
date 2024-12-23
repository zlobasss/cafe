from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QDoubleSpinBox, QCheckBox, QMessageBox
from PyQt5.QtCore import pyqtSignal
from service.menu_item_service import MenuItemService


class MenuItemForm(QWidget):
    switch_to_list_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить позицию меню")
        self.layout = QVBoxLayout()

        # Формат формы
        self.form_layout = QFormLayout()

        # Поля ввода
        self.name_input = QLineEdit(self)
        self.form_layout.addRow(QLabel("Название:"), self.name_input)

        self.price_input = QDoubleSpinBox(self)
        self.price_input.setMinimum(0.01)
        self.price_input.setDecimals(2)
        self.form_layout.addRow(QLabel("Цена:"), self.price_input)

        self.description_input = QLineEdit(self)
        self.form_layout.addRow(QLabel("Описание:"), self.description_input)

        self.is_available_checkbox = QCheckBox("Доступно", self)
        self.is_available_checkbox.setChecked(True)
        self.form_layout.addRow(self.is_available_checkbox)

        self.layout.addLayout(self.form_layout)

        # Кнопки управления
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_item)
        self.layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Отмена", self)
        self.cancel_button.clicked.connect(self.cancel_form)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def save_item(self):
        """Сохраняет новую позицию меню."""
        name = self.name_input.text().strip()
        price = self.price_input.value()
        description = self.description_input.text().strip()
        is_available = self.is_available_checkbox.isChecked()

        if not name or price <= 0:
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля!")
            return

        try:
            MenuItemService.create_menu_item(name, price, description, is_available)
            QMessageBox.information(self, "Успех", "Позиция успешно добавлена!")
            self.switch_to_list_signal.emit()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить позицию: {str(e)}")

    def cancel_form(self):
        """Отменяет добавление позиции и возвращает к списку."""
        self.clear_form()
        self.switch_to_list_signal.emit()

    def clear_form(self):
        """Очищает данные формы."""
        self.name_input.clear()
        self.price_input.setValue(0.01)
        self.description_input.clear()
        self.is_available_checkbox.setChecked(True)
