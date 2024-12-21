from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog, QMessageBox, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from model.user import User
from service.user_service import UserService

class EmployeeForm(QWidget):

    switch_to_list_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавить сотрудника")
        self.setGeometry(100, 100, 600, 500)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        # Поля ввода
        self.first_name_field = QLineEdit(self)
        self.first_name_field.setPlaceholderText("Имя")
        self.layout.addWidget(self.first_name_field)

        self.last_name_field = QLineEdit(self)
        self.last_name_field.setPlaceholderText("Фамилия")
        self.layout.addWidget(self.last_name_field)

        self.second_name_field = QLineEdit(self)
        self.second_name_field.setPlaceholderText("Отчество")
        self.layout.addWidget(self.second_name_field)

        self.contact_details_field = QLineEdit(self)
        self.contact_details_field.setPlaceholderText("Контактные данные")
        self.layout.addWidget(self.contact_details_field)

        # Логин и пароль
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Логин")
        self.layout.addWidget(self.username_field)

        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Пароль")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_field)

        # Роль
        self.role_field = QComboBox(self)
        self.role_field.addItems(["Администратор", "Официант", "Повар"])
        self.layout.addWidget(self.role_field)

        # Загрузка фото
        self.photo_label = QLabel("Фото сотрудника не выбрано", self)
        self.layout.addWidget(self.photo_label)

        self.photo_button = QPushButton("Загрузить фото", self)
        self.photo_button.clicked.connect(self.upload_photo)
        self.layout.addWidget(self.photo_button)

        # Загрузка трудового договора
        self.contract_label = QLabel("Трудовой договор не выбран", self)
        self.layout.addWidget(self.contract_label)

        self.contract_button = QPushButton("Загрузить договор", self)
        self.contract_button.clicked.connect(self.upload_contract)
        self.layout.addWidget(self.contract_button)

        # Кнопка для сохранения
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_employee)
        self.layout.addWidget(self.save_button)

        # Кнопка для отмены
        self.cancel_button = QPushButton("Отмена", self)
        self.cancel_button.clicked.connect(self.close_form)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

        self.photo_path = None
        self.contract_path = None

    def upload_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите фото сотрудника", "", "Изображения (*.png *.jpg *.jpeg)")
        if file_path:
            self.photo_path = file_path
            self.photo_label.setText(f"Фото: {file_path}")

    def upload_contract(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите трудовой договор", "", "Документы (*.pdf *.docx)")
        if file_path:
            self.contract_path = file_path
            self.contract_label.setText(f"Договор: {file_path}")

    def save_employee(self):
        first_name = self.first_name_field.text()
        last_name = self.last_name_field.text()
        second_name = self.second_name_field.text()
        contact_details = self.contact_details_field.text()
        username = self.username_field.text()
        password = self.password_field.text()
        role = self.role_field.currentText()

        if not all([first_name, last_name, role, username, password]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все обязательные поля!")
            return

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            second_name=second_name,
            contact_details=contact_details,
            username=username,
            password=password,
            role=role,
            photo_path=self.photo_path,
            contract_path=self.contract_path
        )

        UserService.create_user(new_user)
        QMessageBox.information(self, "Успех", "Сотрудник успешно добавлен!")
        self.close_form

    def close_form(self):
        self.clear_form()
        self.switch_to_list_signal.emit()

    def clear_form(self):
        self.first_name_field.clear()
        self.last_name_field.clear()
        self.second_name_field.clear()
        self.contact_details_field.clear()
        self.username_field.clear()
        self.password_field.clear()
        self.role_field.setCurrentIndex(0)
        self.photo_label.setText("Фото сотрудника не выбрано")
        self.contract_label.setText("Трудовой договор не выбран")
        self.photo_path = None
        self.contract_path = None
