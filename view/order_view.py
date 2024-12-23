from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from view.order_list import OrderList
from view.order_form import OrderForm
from view.order_card import OrderCard


class OrderView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Заказы")

        # Основной лэйаут
        self.layout = QVBoxLayout()

        # Стек для переключения между представлениями
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # Создаем компоненты
        self.order_list = OrderList(self)  # Передаем self как родительский объект
        self.order_form = OrderForm()

        # Добавляем их в стек
        self.stacked_widget.addWidget(self.order_list)
        self.stacked_widget.addWidget(self.order_form)

        # Подключаем сигналы для переключения форм
        self.order_list.switch_to_form_signal.connect(self.show_order_form)
        self.order_list.switch_to_card_signal.connect(self.show_order_card)
        self.order_form.switch_to_list_signal.connect(self.show_order_list)

        self.setLayout(self.layout)

    def show_order_form(self):
        """Показывает форму создания заказа"""
        self.order_form.load_data()
        self.stacked_widget.setCurrentWidget(self.order_form)

    def show_order_card(self, order):
        """Показывает карточку заказа"""
        self.order_card = OrderCard(order)
        self.order_card.switch_to_list_signal.connect(self.show_order_list)
        self.stacked_widget.addWidget(self.order_card)  # Добавляем карточку в стек
        self.stacked_widget.setCurrentWidget(self.order_card)  # Переключаемся на карточку

    def show_order_list(self):
        """Показывает список заказов"""
        self.order_list.load_orders()
        self.stacked_widget.setCurrentWidget(self.order_list)
