# service/shift_service.py
from model.shift import Shift
from model.shift_employee import ShiftEmployee
from sqlalchemy.orm import Session
from database import Database

db = Database.get_session()

class ShiftService:

    @staticmethod
    def create_shift(shift_date, start_time, end_time, admin_id, employee_ids):
        if not (4 <= len(employee_ids) <= 7):
            raise ValueError("Количество сотрудников в смене должно быть от 4 до 7")

        shift = Shift(shift_date=shift_date, start_time=start_time, end_time=end_time, admin_id=admin_id)
        db.add(shift)
        db.commit()
        db.refresh(shift)

        for user_id in employee_ids:
            shift_employee = ShiftEmployee(shift_id=shift.id, user_id=user_id)
            db.add(shift_employee)
        
        db.commit()
        return shift

    @staticmethod
    def get_shift_by_id(shift_id):
        return db.query(Shift).filter(Shift.id == shift_id).first()

    @staticmethod
    def get_all_shifts(page=1, page_size=10):
        """
        Получить все смены с пагинацией.

        :param page: Номер страницы.
        :param page_size: Количество элементов на странице.
        :return: Словарь с данными смен и общей информацией о пагинации.
        """
        # Вычисление смещения для пагинации
        offset = (page - 1) * page_size
        
        # Получаем смены с учетом пагинации
        shifts = db.query(Shift).offset(offset).limit(page_size).all()

        # Получаем общее количество смен
        total_shifts = db.query(Shift).count()

        # Вычисляем общее количество страниц
        total_pages = (total_shifts + page_size - 1) // page_size  # Округление вверх

        return {
            "shifts": shifts,
            "total_shifts": total_shifts,
            "total_pages": total_pages
        }
