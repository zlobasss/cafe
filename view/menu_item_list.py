from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QAbstractItemView, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from service.menu_item_service import MenuItemService


class MenuItemList(QWidget):
    switch_to_form_signal = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle("Список позиций меню")
        self.layout = QVBoxLayout()

        # Кнопка добавления новой позиции
        self.add_item_button = QPushButton("Добавить позицию", self)
        self.add_item_button.clicked.connect(self.open_add_item_form)
        self.layout.addWidget(self.add_item_button)

        # Таблица позиций меню
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)  # Колонки: ID, Название, Цена, Статус
        self.table_widget.setHorizontalHeaderLabels(["ID", "Название", "Цена", "Статус"])
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
        self.load_items()

    def load_items(self):
        """Загружает позиции меню для текущей страницы."""
        data = MenuItemService.get_menu_items_with_pagination(self.current_page, self.page_size)
        items = data["items"]
        self.total_pages = data["total_pages"]
        self.page_label.setText(f"Страница {self.current_page} из {self.total_pages}")

        self.table_widget.setRowCount(len(items))
        for row, item in enumerate(items):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(item.id)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(item.name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(f"{item.price:.2f}₽"))
            self.table_widget.setItem(row, 3, QTableWidgetItem("Доступно" if item.is_available else "Недоступно"))

    def open_add_item_form(self):
        """Переход к форме добавления позиции."""
        self.switch_to_form_signal.emit()

    def prev_page(self):
        """Переход на предыдущую страницу."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_items()

    def next_page(self):
        """Переход на следующую страницу."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_items()
