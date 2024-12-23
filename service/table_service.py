from model.table import Table
from database import Database

class TableService:
    @staticmethod
    def get_all_tables():
        """Получает все столы из базы данных."""
        session = Database.get_session()
        try:
            return session.query(Table).all()
        finally:
            session.close()

    @staticmethod
    def get_tables_with_pagination(page: int, page_size: int) -> dict:
        """Получает столы с пагинацией."""
        session = Database.get_session()
        try:
            total_tables = session.query(Table).count()
            total_pages = (total_tables + page_size - 1) // page_size
            offset = (page - 1) * page_size
            tables = session.query(Table).offset(offset).limit(page_size).all()

            return {
                "tables": tables,
                "total_pages": total_pages,
                "current_page": page
            }
        finally:
            session.close()

    @staticmethod
    def create_table(table_name: str, capacity: int):
        """Создает новый стол."""
        session = Database.get_session()
        try:
            new_table = Table(table_name=table_name, capacity=capacity)
            session.add(new_table)
            session.commit()
            return new_table
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_table(table_id: int):
        """Удаляет стол."""
        session = Database.get_session()
        try:
            table = session.query(Table).filter(Table.id == table_id).first()
            if not table:
                raise ValueError("Стол не найден.")
            session.delete(table)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def update_table(table_id: int, table_name: str, capacity: int):
        """Обновляет данные стола."""
        session = Database.get_session()
        try:
            table = session.query(Table).filter(Table.id == table_id).first()
            if not table:
                raise ValueError("Стол не найден.")
            table.table_name = table_name
            table.capacity = capacity
            session.commit()
            return table
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_table_by_id(table_id: int) -> Table:
        session = Database.get_session()
        try:
            table = session.query(Table).filter(Table.id == table_id).first()
            return table
        except Exception as e:
            raise e
        finally:
            session.close()
