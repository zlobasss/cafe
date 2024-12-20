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
            QMessageBox.information(self, "Успех", "Авторизация успешна!")
            self.show_main_view()  # Переход к главному окну
        else:
            QMessageBox.warning(self, "Ошибка", "Неверные данные!")

    def show_main_view(self):
        # Скрытие текущего окна (экран авторизации)
        self.hide()

        self.main_view.show()

def main():
    app = QApplication(sys.argv)
    login_view = LoginView()
    login_view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
