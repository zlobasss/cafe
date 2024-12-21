from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .shift import Shift
from .shift_employee import ShiftEmployee

