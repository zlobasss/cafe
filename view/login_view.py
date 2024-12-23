# view/login_view.py

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QSizePolicy
from PyQt5.QtCore import Qt, QFile, QTextStream
from model.user import Role
import sys

class LoginView(QWidget):
    def __init__(self, login_view_model):
        super().__init__()

        self.login_view_model = login_view_model

        self.setWindowTitle("Авторизация")
        self.setGeometry(100, 100, 600, 450)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.apply_styles()

        self.empty_first = QLabel("", self)
        self.layout.addWidget(self.empty_first)

        self.title = QLabel("Авторизация", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Введите логин")
        self.layout.addWidget(self.username_field)

        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Введите пароль")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_field)

        self.login_button = QPushButton("Войти", self)
        self.login_button.clicked.connect(self.authenticate_user)
        self.layout.addWidget(self.login_button)

        self.empty_last = QLabel("", self)
        self.layout.addWidget(self.empty_last)

        self.setLayout(self.layout)

        self.show()
        if self.check_session():
            self.show_main_view()

    def apply_styles(self):
        file = QFile("./resources/style/main_styles.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = QTextStream(file).readAll()
            self.setStyleSheet(stylesheet)
        else:
            print("Ошибка при загрузке стилей")

    def authenticate_user(self):
        username = self.username_field.text()
        password = self.password_field.text()

        try:
            message = self.login_view_model.authenticate_user(username, password)
            if not self.check_session():
                raise ValueError("У вас нету сейчас текущих смен")
            QMessageBox.information(self, "Успех", message)
            self.show_main_view()
        except ValueError as e:
            self.show()
            QMessageBox.warning(self, "Ошибка", str(e))

    def check_session(self):
        user = self.login_view_model.get_authenticated_user()
        shifts = self.login_view_model.get_user_shifts(user)
        print (shifts.__len__())
        if user and (shifts.__len__() != 0 or user.role == Role.ADMIN):
            return True
        else:
            return False

    def show_main_view(self):
        self.close()
        from view.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
