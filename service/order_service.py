from model.order import Order, OrderStatus
from model.menu_item import MenuItem
from model.order_item import OrderItem
from service.shift_service import ShiftService
from database import Database


class OrderService:
    @staticmethod
    def create_order(waiter_id, table_id, menu_items):
        session = Database.get_session()
        
        try:
            print("Waiter id: " + waiter_id.__str__())
            shift = ShiftService.get_shifts_by_user_id(waiter_id)

            order = Order(waiter_id=waiter_id, shift_id=shift.pop().shift_id, table_id=table_id, status=OrderStatus.ACCEPTED)
            session.add(order)
            session.commit()

            total_amount = 0
            for item in menu_items:
                menu_item = session.query(MenuItem).get(item['menu_item_id'])
                if not menu_item.is_available:
                    raise ValueError(f"Блюдо {menu_item.name} недоступно")
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item.id,
                    quantity=item['quantity'],
                    item_total=menu_item.price * item['quantity']
                )
                total_amount += order_item.item_total
                session.add(order_item)

            order.total_amount = total_amount
            session.commit()
            return order
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def get_orders_with_pagination(page: int, page_size: int) -> dict:
        session = Database.get_session()
        try:
            total_orders = session.query(Order).count()
            total_pages = (total_orders + page_size - 1) // page_size
            offset = (page - 1) * page_size
            orders = session.query(Order).offset(offset).limit(page_size).all()

            return {
                "orders": orders,
                "total_pages": total_pages,
                "current_page": page
            }
        finally:
            session.close()

    @staticmethod
    def get_order_by_id(order_id: int):
        session = Database.get_session()
        try:
            return session.query(Order).filter(Order.id == order_id).first()
        finally:
            session.close()

    @staticmethod
    def get_order_items(order_id: int):
        """Возвращает позиции конкретного заказа."""
        session = Database.get_session()
        try:
            return session.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        finally:
            session.close()

    @staticmethod
    def change_order_status(order_id: int):
        """Изменяет статус заказа на следующий."""
        session = Database.get_session()
        try:
            order = session.query(Order).filter(Order.id == order_id).first()
            if not order:
                raise ValueError("Заказ не найден.")

            status_sequence = OrderStatus._member_names_
            current_index = status_sequence.index(order.status.name)
            if current_index < len(status_sequence) - 1:
                order.status = status_sequence[current_index + 1]
            else:
                raise ValueError("Статус заказа уже окончательный.")

            session.commit()
            return order.status
        finally:
            session.close()