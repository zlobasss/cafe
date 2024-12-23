# main.py
from view.login_view import LoginView
from viewmodel.login_view_model import LoginViewModel
from service.user_service import UserService
from util.session_manager import SessionManager
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    main_window = LoginView(login_view_model=LoginViewModel(UserService(), SessionManager()))
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
