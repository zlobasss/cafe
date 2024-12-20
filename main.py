# main.py
from view.login_view import LoginView
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    login_view = LoginView()
    login_view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
