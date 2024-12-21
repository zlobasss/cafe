#view/employee_list.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QAbstractItemView, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt, QFile, QTextStream, pyqtSignal
from service.user_service import UserService
from view.employee_card import EmployeeCard  # Импортируем класс для карточки сотрудника

class EmployeeList(QWidget):

    switch_to_form_signal = pyqtSignal()
    switch_to_card_signal = pyqtSignal(object)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.parentWidget = parent
        self.setWindowTitle("Сотрудники")
        self.layout = QVBoxLayout()

        self.apply_styles()

        # Кнопка добавления сотрудника
        self.add_employee_button = QPushButton("Добавить сотрудника", self)
        self.add_employee_button.setObjectName("save_button")  # Устанавливаем имя объекта для применения стиля
        self.add_employee_button.clicked.connect(self.open_add_employee_form)
        self.layout.addWidget(self.add_employee_button)

        # Таблица сотрудников
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(6)  # Фамилия, Имя, Отчество, Роль, Контакты, Статус
        self.table_widget.setHorizontalHeaderLabels(
            ["Фамилия", "Имя", "Отчество", "Роль", "Контакты", "Статус"]
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
        self.load_users()

        # Обработчик двойного клика по таблице
        self.table_widget.doubleClicked.connect(self.open_employee_card)

    def open_add_employee_form(self):
        self.switch_to_form_signal.emit()

    
    def open_employee_card(self):
        """Открывает карточку сотрудника при двойном клике на строку в таблице."""
        row = self.table_widget.currentRow()
        user_id = self.table_widget.item(row, 0).data(Qt.UserRole)  # Получаем ID сотрудника

        if user_id:
            user = UserService.get_user_by_id(user_id)
            if user:
                # Открываем карточку сотрудника
                self.switch_to_card_signal.emit(user)
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось найти сотрудника.")

    def load_users(self):
        """Загружает пользователей для текущей страницы и обновляет таблицу."""
        data = UserService.get_users_with_pagination(self.current_page, self.page_size)

        users = data["users"]
        self.total_pages = data["total_pages"]
        self.page_label.setText(f"Страница {self.current_page} из {self.total_pages}")

        self.table_widget.setRowCount(len(users))
        for row, user in enumerate(users):
            self.table_widget.setItem(row, 0, QTableWidgetItem(user.last_name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(user.first_name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(user.second_name))
            self.table_widget.setItem(row, 3, QTableWidgetItem(user.role.value))
            self.table_widget.setItem(row, 4, QTableWidgetItem(user.contact_details))
            self.table_widget.setItem(row, 5, QTableWidgetItem("Работает" if user.is_active else "Уволен"))

            # Сохраняем ID в UserRole (скрытая информация)
            item = self.table_widget.item(row, 0)
            item.setData(Qt.UserRole, user.id)

        # Управление кнопками пагинации
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < self.total_pages)

    def prev_page(self):
        """Переход на предыдущую страницу."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_users()

    def next_page(self):
        """Переход на следующую страницу."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_users()

    def apply_styles(self):
        file = QFile("./resources/style/main_styles.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(file).readAll()
            self.setStyleSheet(stylesheet)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить файл стилей")
