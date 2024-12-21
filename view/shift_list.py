# view/shift_list.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QAbstractItemView, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt, QFile, QTextStream, pyqtSignal
from service.shift_service import ShiftService
from service.user_service import UserService

class ShiftList(QWidget):

    switch_to_form_signal = pyqtSignal()

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.parentWidget = parent
        self.setWindowTitle("Смены")
        self.layout = QVBoxLayout()

        self.apply_styles()

        # Кнопка добавления смены
        self.add_shift_button = QPushButton("Создать смену", self)
        self.add_shift_button.setObjectName("save_button")  # Устанавливаем имя объекта для применения стиля
        self.add_shift_button.clicked.connect(self.open_add_shift_form)
        self.layout.addWidget(self.add_shift_button)

        # Таблица смен
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(
            ["Дата", "Начало смены", "Конец смены", "Ответственный"]
        )

        # Запрещаем редактирование таблицы
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Настройка растягивания столбцов
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # Все столбцы будут растягиваться одинаково

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
        self.load_shifts()

    def open_add_shift_form(self):
        self.switch_to_form_signal.emit()

    def load_shifts(self):
        """Загружает смены для текущей страницы и обновляет таблицу."""
        data = ShiftService.get_all_shifts(self.current_page, self.page_size)

        shifts = data["shifts"]
        self.total_pages = data["total_pages"]
        self.page_label.setText(f"Страница {self.current_page} из {self.total_pages}")

        self.table_widget.setRowCount(len(shifts))
        for row, shift in enumerate(shifts):
            self.table_widget.setItem(row, 0, QTableWidgetItem(shift.shift_date.isoformat()))
            self.table_widget.setItem(row, 1, QTableWidgetItem(shift.start_time.isoformat()))
            self.table_widget.setItem(row, 2, QTableWidgetItem(shift.end_time.isoformat()))
            responsible = UserService.get_user_by_id(shift.admin_id)
            responsible_name = responsible.last_name + ' ' + responsible.first_name
            self.table_widget.setItem(row, 3, QTableWidgetItem(responsible_name))

        # Управление кнопками пагинации
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < self.total_pages)

    def prev_page(self):
        """Переход на предыдущую страницу."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_shifts()

    def next_page(self):
        """Переход на следующую страницу."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_shifts()

    def apply_styles(self):
        file = QFile("./resources/style/main_styles.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(file).readAll()
            self.setStyleSheet(stylesheet)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить файл стилей")
