from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QAbstractItemView, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from service.order_service import OrderService
from service.table_service import TableService
from service.user_service import UserService
from model.user import Role

class OrderList(QWidget):
    switch_to_form_signal = pyqtSignal()
    switch_to_card_signal = pyqtSignal(object)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle("Список заказов")
        self.layout = QVBoxLayout()

        current_user = UserService.get_session_user()
        if (current_user.role == Role.WAITER):
            # Кнопка создания нового заказа
            self.add_order_button = QPushButton("Создать заказ", self)
            self.add_order_button.clicked.connect(self.open_add_order_form)
            self.layout.addWidget(self.add_order_button)

        # Таблица заказов
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(5)  # Колонки: Номер, Столик, Официант, Статус, Сумма
        self.table_widget.setHorizontalHeaderLabels(["Номер", "Столик", "Официант", "Статус", "Сумма"])
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table_widget)

        # Навигация страниц
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Назад", self)
        self.prev_button.clicked.connect(self.prev_page)
        self.pagination_layout.addWidget(self.prev_button)

        self.page_label = QLabel("Страница 1", self)
        self.pagination_layout.addWidget(self.page_label, alignment=Qt.AlignCenter)

        self.next_button = QPushButton("Вперед", self)
        self.next_button.clicked.connect(self.next_page)
        self.pagination_layout.addWidget(self.next_button)
        self.layout.addLayout(self.pagination_layout)

        self.setLayout(self.layout)

        # Инициализация пагинации
        self.current_page = 1
        self.page_size = 10
        self.load_orders()

        # Обработчик двойного клика по строке
        self.table_widget.doubleClicked.connect(self.open_order_card)

    def load_orders(self):
        """Загружает заказы для текущей страницы и обновляет таблицу."""
        data = OrderService.get_orders_with_pagination(self.current_page, self.page_size)
        orders = data["orders"]
        self.total_pages = data["total_pages"]
        self.page_label.setText(f"Страница {self.current_page} из {self.total_pages}")

        self.table_widget.setRowCount(len(orders))
        for row, order in enumerate(orders):
            table_name = TableService.get_table_by_id(order.table_id).table_name
            waiter = UserService.get_user_by_id(order.waiter_id)
            waiter_name = waiter.last_name + ' ' + waiter.first_name
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(order.id)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(table_name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(waiter_name))
            self.table_widget.setItem(row, 3, QTableWidgetItem(order.status.value))
            self.table_widget.setItem(row, 4, QTableWidgetItem(f"{order.total_amount:.2f}"))

    def open_add_order_form(self):
        """Переход к форме добавления заказа."""
        self.switch_to_form_signal.emit()

    def open_order_card(self):
        """Открывает карточку заказа при двойном клике."""
        row = self.table_widget.currentRow()
        order_id = self.table_widget.item(row, 0).text()
        order = OrderService.get_order_by_id(order_id)
        if order:
            self.switch_to_card_signal.emit(order)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные заказа.")

    def prev_page(self):
        """Переход на предыдущую страницу."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_orders()

    def next_page(self):
        """Переход на следующую страницу."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_orders()
