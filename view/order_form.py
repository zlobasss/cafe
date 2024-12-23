from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QComboBox, QMessageBox
)
from PyQt5.QtCore import pyqtSignal
from service.order_service import OrderService
from service.menu_item_service import MenuItemService
from service.table_service import TableService
from service.user_service import UserService


class OrderForm(QWidget):
    switch_to_list_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Создать заказ")
        self.layout = QVBoxLayout()

        # Формат формы
        self.form_layout = QFormLayout()

        # Поля ввода
        self.table_select = QComboBox(self)
        self.form_layout.addRow(QLabel("Столик:"), self.table_select)

        self.customer_count = QSpinBox(self)
        self.customer_count.setMinimum(1)
        self.form_layout.addRow(QLabel("Количество клиентов:"), self.customer_count)

        self.menu_item_select = QComboBox(self)
        self.form_layout.addRow(QLabel("Позиция меню:"), self.menu_item_select)

        self.quantity = QSpinBox(self)
        self.quantity.setMinimum(1)
        self.form_layout.addRow(QLabel("Количество:"), self.quantity)

        self.add_item_button = QPushButton("Добавить позицию", self)
        self.add_item_button.clicked.connect(self.add_menu_item)
        self.form_layout.addWidget(self.add_item_button)

        self.layout.addLayout(self.form_layout)

        # Кнопки управления
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_order)
        self.layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Отмена", self)
        self.cancel_button.clicked.connect(self.cancel_form)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

        # Хранение позиций заказа
        self.order_items = []
        self.load_data()

    def load_data(self):
        """Загружает данные столов и меню."""
        try:
            tables = TableService.get_all_tables()
            menu_items = MenuItemService.get_all_menu_items()

            self.table_select.clear()
            for table in tables:
                self.table_select.addItem(table.table_name, table.id)

            self.menu_item_select.clear()
            for item in menu_items:
                if item.is_available:
                    self.menu_item_select.addItem(f"{item.name} - {item.price:.2f}₽", item.id)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def add_menu_item(self):
        """Добавляет выбранную позицию меню в заказ."""
        item_id = self.menu_item_select.currentData()
        quantity = self.quantity.value()

        if not item_id or quantity <= 0:
            QMessageBox.warning(self, "Ошибка", "Выберите позицию меню и укажите количество!")
            return

        item_name = self.menu_item_select.currentText().split(" - ")[0]
        self.order_items.append({"menu_item_id": item_id, "quantity": quantity})
        QMessageBox.information(self, "Успех", f"Добавлено: {item_name}, Количество: {quantity}")

    def save_order(self):
        """Сохраняет заказ."""
        table_id = self.table_select.currentData()
        customer_count = self.customer_count.value()
        waiter_id = UserService.get_session_user().id

        if not table_id or customer_count <= 0 or not self.order_items:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля и добавьте хотя бы одну позицию!")
            return

        try:
            OrderService.create_order(waiter_id, table_id, self.order_items)
            QMessageBox.information(self, "Успех", "Заказ успешно создан!")
            self.switch_to_list_signal.emit()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать заказ: {str(e)}")

    def cancel_form(self):
        """Отменяет создание заказа и возвращает к списку."""
        self.clear_form()
        self.switch_to_list_signal.emit()

    def clear_form(self):
        """Очищает данные формы."""
        self.table_select.setCurrentIndex(0)
        self.customer_count.setValue(1)
        self.menu_item_select.setCurrentIndex(0)
        self.quantity.setValue(1)
        self.order_items.clear()
