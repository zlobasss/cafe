#view/main_window.py

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QSpacerItem, QSizePolicy, QMessageBox, QLabel)
from PyQt5.QtCore import QFile, QTextStream
from view.employees_view import EmployeesView
from view.login_view import LoginView
from view.shift_view import ShiftView
from service.user_service import UserService

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.new_nav_text = QLabel("Раздел: ")
        self.old_nav_text = QLabel("Раздел: Сотрудники")

        self.setWindowTitle("Главное окно")
        self.showFullScreen()
        self.setGeometry(100, 100, 1000, 600)

        self.apply_styles()

        # Основной вертикальный layout
        self.main_layout = QVBoxLayout()

        # Горизонтальный layout для содержимого и разделов
        self.content_layout = QHBoxLayout()
        
        # Создаем QStackedWidget для контента
        self.stacked_widget = QStackedWidget(self)

        # Список с виджетами и их названиями
        self.views = [
            ("Сотрудники", EmployeesView()),
            ("Смены", ShiftView())
        ]

        # Панель с кнопками для перехода между разделами
        self.sidebar_layout = QVBoxLayout()

        # Верхняя горизонтальная панель
        self.navbar_layout = QHBoxLayout()

        # Добавляем кнопку "Выход" в navbar
        self.add_logout_button()

        # Добавляем виджеты и кнопки динамически
        for label, widget in self.views:
            self.add_button(label, widget)

        # Добавление пустого пространства для подгонки кнопок в панели
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sidebar_layout.addItem(spacer)

        # Добавляем панель с кнопками и основной контент в основной layout
        self.main_layout.addLayout(self.navbar_layout, 5)
        self.content_layout.addWidget(self.stacked_widget, 85)
        self.content_layout.addLayout(self.sidebar_layout, 15)
        self.main_layout.addLayout(self.content_layout, 95)

        self.setLayout(self.main_layout)

    def add_button(self, label: str, widget: QWidget):
        # Добавляем виджет в stacked_widget
        self.stacked_widget.addWidget(widget)
        # Создаем кнопку и подключаем ее к переключению между виджетами
        button = QPushButton(label, self)
        button.clicked.connect(lambda: self.set_widget(label, widget))
        # Добавляем кнопку в боковую панель
        self.sidebar_layout.addWidget(button)

    def set_widget(self, label: str, widget: QWidget):
        # Меняем текущий виджет в QStackedWidget
        self.stacked_widget.setCurrentWidget(widget)
        self.new_nav_text = QLabel("Раздел: " + label)
        self.navbar_layout.replaceWidget(self.old_nav_text, self.new_nav_text)
        self.old_nav_text = self.new_nav_text
        self.navbar_layout.update()

    def add_logout_button(self):
        # Кнопка "Выход"
        logout_button = QPushButton("Выход", self)
        logout_button.setObjectName("cancel_button")  # Устанавливаем имя объекта для применения стиля
        logout_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Фиксированный размер кнопки
        logout_button.setMinimumSize(200, 20)
        logout_button.clicked.connect(self.logout)

        # Текст приветствия
        user = UserService.get_session_user()
        if not user:
            self.logout
            return
        
        hello_text = QLabel("Приветствую, " + user.first_name + ' ' + user.last_name, self)
        hello_text.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Фиксированный размер текста

        empty_label = QLabel("")
        empty_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # Добавляем элементы в navbar с выравниванием справа
        self.navbar_layout.addWidget(self.old_nav_text)
        self.navbar_layout.addWidget(empty_label)
        self.navbar_layout.addWidget(hello_text)
        self.navbar_layout.addWidget(logout_button)

    def logout(self):
        # Очистить содержимое session.txt
        with open("session.txt", "w") as file:
            file.write("")
        
        # Закрыть текущее окно и открыть окно авторизации
        self.close()
        self.login_view = LoginView()
        self.login_view.show()

    def apply_styles(self):
        file = QFile("./resources/style/main_styles.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(file).readAll()
            self.setStyleSheet(stylesheet)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить файл стилей")