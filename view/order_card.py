from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from service.order_service import OrderService
from service.table_service import TableService
from service.user_service import UserService
from service.menu_item_service import MenuItemService


class OrderCard(QWidget):
    switch_to_list_signal = pyqtSignal()

    def __init__(self, order):
        super().__init__()

        self.order = order
        self.setWindowTitle(f"Детали заказа №{order.id}")

        # Основной лэйаут
        self.layout = QVBoxLayout()

        # Информация о заказе
        table_name = TableService.get_table_by_id(order.table_id).table_name
        waiter = UserService.get_user_by_id(order.waiter_id)
        waiter_name = waiter.last_name + ' ' + waiter.first_name

        self.layout.addWidget(QLabel(f"Номер заказа: {order.id}"))
        self.layout.addWidget(QLabel(f"Столик: {table_name}"))
        self.layout.addWidget(QLabel(f"Официант: {waiter_name}"))
        self.layout.addWidget(QLabel(f"Дата и время: {order.created_at.strftime('%Y-%m-%d %H:%M')}"))
        self.layout.addWidget(QLabel(f"Статус: {order.status.value}"))
        self.layout.addWidget(QLabel(f"Общая сумма: {order.total_amount:.2f}₽"))

        # Таблица позиций заказа
        self.item_table = QTableWidget(self)
        self.item_table.setColumnCount(4)  # Позиция, количество, цена, сумма
        self.item_table.setHorizontalHeaderLabels(["Позиция", "Количество", "Цена", "Сумма"])
        self.item_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.item_table)

        self.load_order_items()

        # Кнопки управления
        self.buttons_layout = QHBoxLayout()

        self.back_button = QPushButton("Назад", self)
        self.back_button.clicked.connect(self.go_back)
        self.buttons_layout.addWidget(self.back_button)

        self.change_status_button = QPushButton("Изменить статус", self)
        self.change_status_button.clicked.connect(self.change_order_status)
        self.buttons_layout.addWidget(self.change_status_button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

    def load_order_items(self):
        """Загружает и отображает позиции заказа."""
        items = OrderService.get_order_items(self.order.id)
        self.item_table.setRowCount(len(items))

        for row, item in enumerate(items):
            menu_item = MenuItemService.get_menu_item(item.menu_item_id)
            self.item_table.setItem(row, 0, QTableWidgetItem(menu_item.name))
            self.item_table.setItem(row, 1, QTableWidgetItem(str(item.quantity)))
            self.item_table.setItem(row, 2, QTableWidgetItem(f"{menu_item.price:.2f}₽"))
            self.item_table.setItem(row, 3, QTableWidgetItem(f"{item.item_total:.2f}₽"))

    def change_order_status(self):
        """Изменяет статус заказа."""
        try:
            new_status = OrderService.change_order_status(self.order.id)
            QMessageBox.information(self, "Успех", f"Статус заказа обновлен: {new_status.value}")
            self.order.status = new_status.name
            self.layout.itemAt(4).widget().setText(f"Статус: {new_status.value}")  # Обновление виджета статуса
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить статус: {str(e)}")

    def go_back(self):
        """Возвращает к списку заказов."""
        self.switch_to_list_signal.emit()
