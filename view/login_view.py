from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt, QFile, QTextStream
from service.user_service import UserService
import sys

class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Авторизация")
        self.setGeometry(100, 100, 600, 450)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Центрирование виджетов в макете

        # Загрузка и применение стилей из файла
        self.apply_styles()

        self.empty_first = QLabel("", self)
        self.layout.addWidget(self.empty_first)

        # Заголовок
        self.title = QLabel("Авторизация", self)
        self.title.setAlignment(Qt.AlignCenter)  # Центрирование текста и вертикально, и горизонтально
        self.layout.addWidget(self.title)

        # Поле для логина
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Введите логин")
        self.layout.addWidget(self.username_field)

        # Поле для пароля
        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Введите пароль")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_field)

        # Кнопка авторизации
        self.login_button = QPushButton("Войти", self)
        self.login_button.clicked.connect(self.authenticate_user)
        self.layout.addWidget(self.login_button)

        self.empty_last = QLabel("", self)
        self.layout.addWidget(self.empty_last)

        self.setLayout(self.layout)

        self.check_session()
        

    def apply_styles(self):
        file = QFile("./resources/style/main_styles.qss")  # Убедитесь, что файл находится в той же директории или укажите полный путь
        if file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(file).readAll()
            self.setStyleSheet(stylesheet)
        else:
            print("Ошибка при загрузке стилей")

    def authenticate_user(self):
        username = self.username_field.text()
        password = self.password_field.text()

        # Проверка на пустые поля
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        # Логика авторизации через запрос к БД через viewmodel
        user = UserService.find_by_username(username)

        if user and UserService.verify_password(user.password, password):
            if not user.is_active:
                QMessageBox.warning(self, "Ошибка", "Вы были уволены!")
                return
            token = UserService.generate_token(user.id)
            QMessageBox.information(self, "Успех", "Авторизация успешна!")
            self.store_session(token)  # Сохранение токена в сессии
            self.check_session()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверные данные!")

    def store_session(self, token: str):
        with open("session.txt", "w") as file:
            file.write(token)

    def check_session(self):
        try:
            with open("session.txt", "r") as file:
                token = file.read()
            payload = UserService.verify_token(token)
            user_id = payload["user_id"]
            # Если токен валиден, сразу переходим в главное окно
            self.show_main_view()
            return True
        except (FileNotFoundError, ValueError):
            # Если токен отсутствует или невалиден, показываем экран авторизации
            print("Сессия неактивна")
            self.show()
            return False

    def show_main_view(self):
        # Скрытие текущего окна (экран авторизации)
        self.close()

        from view.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
