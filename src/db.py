from os import environ
from pathlib import Path
from typing import Generator

from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

# Use environment variable or default to data/tasks.db in parent directory
db_path = environ.get(
    "TEXTING_REMINDERS_TASK_DB_PATH",
    str(Path(__file__).parent.parent / "data" / "tasks.db")
)

engine = create_engine(f"sqlite:///{db_path}")
SessionLocal = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Database session dependency for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
