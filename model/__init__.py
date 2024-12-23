#model/__init__.py

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .shift import Shift
from .shift_employee import ShiftEmployee
from .menu_item import MenuItem
from .table import Table
from .order import Order
from .order_item import OrderItem

