#view/main_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QSpacerItem, QSizePolicy, QLabel, QMessageBox
from PyQt5.QtCore import QFile, QTextStream
from view.login_view import LoginView
from viewmodel.main_view_model import MainViewModel  # Импорт ViewModel
from viewmodel.login_view_model import LoginViewModel
from service.user_service import UserService
from util.session_manager import SessionManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.view_model = MainViewModel()

        self.old_nav_text = QLabel("Раздел: " + self.view_model.get_views().copy().pop()[0])

        self.view_model.user_updated.connect(self.update_user_ui)  # Подключаем сигнал обновления UI

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

        # Панель с кнопками для перехода между разделами
        self.sidebar_layout = QVBoxLayout()

        # Верхняя горизонтальная панель
        self.navbar_layout = QHBoxLayout()

        self.add_logout_button()

        # Загружаем представления из ViewModel
        for label, widget in self.view_model.get_views():
            self.add_button(label, widget)

        # Добавление пустого пространства для подгонки кнопок в панели
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sidebar_layout.addItem(spacer)

        # Добавляем панель с кнопками и основной контент в основной layout
        self.main_layout.addLayout(self.navbar_layout, 5)
        self.main_layout.addWidget(self.stacked_widget, 95)
        self.content_layout.addLayout(self.main_layout, 85)
        self.content_layout.addLayout(self.sidebar_layout, 15)

        self.setLayout(self.content_layout)

        # Загружаем пользователя через ViewModel
        self.view_model.load_user()

    def update_user_ui(self, message: str):
        """Обновление UI после загрузки/выхода пользователя"""
        hello_text = QLabel(message, self)
        hello_text.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        empty_label = QLabel(" ")
        empty_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.navbar_layout.addWidget(self.old_nav_text)
        self.navbar_layout.addWidget(empty_label)
        self.navbar_layout.addWidget(hello_text)
        self.navbar_layout.update()

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
        logout_button.setMinimumSize(200, 20)
        logout_button.clicked.connect(self.logout)
        self.sidebar_layout.addWidget(logout_button)

    def logout(self):
        self.view_model.logout()
        self.close()

        # Инициализируем LoginView с нужной моделью
        user_service = UserService()
        session_manager = SessionManager()
        login_view_model = LoginViewModel(user_service, session_manager)

        # Передаем login_view_model в LoginView
        self.login_view = LoginView(login_view_model=login_view_model)
        self.login_view.show()


    def apply_styles(self):
        file = QFile("./resources/style/main_styles.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(file).readAll()
            self.setStyleSheet(stylesheet)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить файл стилей")
