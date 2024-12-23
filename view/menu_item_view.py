from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from view.menu_item_list import MenuItemList
from view.menu_item_form import MenuItemForm


class MenuItemView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Позиции меню")

        # Основной лэйаут
        self.layout = QVBoxLayout()

        # Стек для переключения между представлениями
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # Создаем компоненты
        self.menu_item_list = MenuItemList(self)
        self.menu_item_form = MenuItemForm()

        # Добавляем их в стек
        self.stacked_widget.addWidget(self.menu_item_list)
        self.stacked_widget.addWidget(self.menu_item_form)

        # Подключаем сигналы для переключения форм
        self.menu_item_list.switch_to_form_signal.connect(self.show_menu_item_form)
        self.menu_item_form.switch_to_list_signal.connect(self.show_menu_item_list)

        self.setLayout(self.layout)

    def show_menu_item_form(self):
        """Показывает форму добавления позиции меню."""
        self.stacked_widget.setCurrentWidget(self.menu_item_form)

    def show_menu_item_list(self):
        """Показывает список позиций меню."""
        self.menu_item_list.load_items()
        self.stacked_widget.setCurrentWidget(self.menu_item_list)
