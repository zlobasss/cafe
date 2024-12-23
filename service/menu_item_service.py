from model.menu_item import MenuItem
from database import Database

class MenuItemService:
    @staticmethod
    def get_all_menu_items():
        """Получает все доступные позиции меню."""
        session = Database.get_session()
        try:
            return session.query(MenuItem).filter(MenuItem.is_available == True).all()
        finally:
            session.close()

    @staticmethod
    def get_menu_items_with_pagination(page: int, page_size: int) -> dict:
        """Получает позиции меню с пагинацией."""
        session = Database.get_session()
        try:
            total_items = session.query(MenuItem).count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page - 1) * page_size
            items = session.query(MenuItem).offset(offset).limit(page_size).all()

            return {
                "items": items,
                "total_pages": total_pages,
                "current_page": page
            }
        finally:
            session.close()

    @staticmethod
    def get_menu_item(menu_item_id: int):
        """Возвращает позиции конкретного заказа."""
        session = Database.get_session()
        try:
            return session.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        finally:
            session.close()

    @staticmethod
    def create_menu_item(name: str, price: float, description: str, is_available: bool):
        """Создает новую позицию меню."""
        session = Database.get_session()
        try:
            new_item = MenuItem(
                name=name, price=price, description=description, is_available=is_available
            )
            session.add(new_item)
            session.commit()
            return new_item
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def update_menu_item(item_id: int, name: str, price: float, description: str, is_available: bool):
        """Обновляет данные позиции меню."""
        session = Database.get_session()
        try:
            item = session.query(MenuItem).filter(MenuItem.id == item_id).first()
            if not item:
                raise ValueError("Позиция меню не найдена.")
            item.name = name
            item.price = price
            item.description = description
            item.is_available = is_available
            session.commit()
            return item
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_menu_item(item_id: int):
        """Удаляет позицию меню."""
        session = Database.get_session()
        try:
            item = session.query(MenuItem).filter(MenuItem.id == item_id).first()
            if not item:
                raise ValueError("Позиция меню не найдена.")
            session.delete(item)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()