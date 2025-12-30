from db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Date, Time, func
from datetime import datetime, date, time

class Task(Base):
    DESCRIPTION_MAX_LEN = 255
    
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(DESCRIPTION_MAX_LEN))
    created_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    deadline_date: Mapped[date| None] = mapped_column(
        Date(),
        nullable=True
    )
    deadline_time: Mapped[time | None] = mapped_column(
        Time(),
        nullable=True
    )
    completed: Mapped[bool] = mapped_column(default=False, index=True)

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, description={self.description!r})"

    def __str__(self) -> str:
        return self.description
