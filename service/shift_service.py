# service/shift_service.py

from model.shift import Shift
from model.shift_employee import ShiftEmployee
from model.user import User
from database import Database
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from sqlalchemy import and_

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
    def get_shifts_by_user_id(user_id):
        current_time = datetime.now()
        current_date = datetime.now().date()
        start_buffer = current_time - timedelta(hours=1)
        end_buffer = current_time + timedelta(hours=1)

        shifts = (
            db.query(ShiftEmployee)
            .join(Shift, Shift.id == ShiftEmployee.shift_id)
            .filter(
                ShiftEmployee.user_id == user_id,
                Shift.shift_date == current_date,
                Shift.start_time <= start_buffer.time(),  # Время начала меньше текущего минус 1 час
                Shift.end_time >= end_buffer.time()       # Время окончания больше текущего плюс 1 час
            )
            .options(joinedload(ShiftEmployee.shift))  # Подгружает связанные смены
            .all()
        )
        return shifts
    
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
