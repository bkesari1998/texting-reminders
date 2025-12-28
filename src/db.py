from os import environ

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

engine = create_engine(f"sqlite:///{environ["TEXTING_REMINDERS_TASK_DB_PATH"]}")
