from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QAbstractItemView, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from service.table_service import TableService


class TableList(QWidget):
    switch_to_form_signal = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle("Список столов")
        self.layout = QVBoxLayout()

        # Кнопка добавления нового стола
        self.add_table_button = QPushButton("Добавить стол", self)
        self.add_table_button.clicked.connect(self.open_add_table_form)
        self.layout.addWidget(self.add_table_button)

        # Таблица столов
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)  # Колонки: Номер, Название, Вместимость
        self.table_widget.setHorizontalHeaderLabels(["ID", "Название", "Вместимость"])
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
        self.load_tables()

    def load_tables(self):
        """Загружает столы для текущей страницы и обновляет таблицу."""
        data = TableService.get_tables_with_pagination(self.current_page, self.page_size)
        tables = data["tables"]
        self.total_pages = data["total_pages"]
        self.page_label.setText(f"Страница {self.current_page} из {self.total_pages}")

        self.table_widget.setRowCount(len(tables))
        for row, table in enumerate(tables):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(table.id)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(table.table_name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(table.capacity)))

    def open_add_table_form(self):
        """Переход к форме добавления стола."""
        self.switch_to_form_signal.emit()

    def prev_page(self):
        """Переход на предыдущую страницу."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_tables()

    def next_page(self):
        """Переход на следующую страницу."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_tables()
