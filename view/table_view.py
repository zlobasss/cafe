from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from view.table_list import TableList
from view.table_form import TableForm


class TableView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Столы")

        # Основной лэйаут
        self.layout = QVBoxLayout()

        # Стек для переключения между представлениями
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # Создаем компоненты
        self.table_list = TableList(self)
        self.table_form = TableForm()

        # Добавляем их в стек
        self.stacked_widget.addWidget(self.table_list)
        self.stacked_widget.addWidget(self.table_form)

        # Подключаем сигналы для переключения форм
        self.table_list.switch_to_form_signal.connect(self.show_table_form)
        self.table_form.switch_to_list_signal.connect(self.show_table_list)

        self.setLayout(self.layout)

    def show_table_form(self):
        """Показывает форму добавления стола."""
        self.stacked_widget.setCurrentWidget(self.table_form)

    def show_table_list(self):
        """Показывает список столов."""
        self.table_list.load_tables()
        self.stacked_widget.setCurrentWidget(self.table_list)
