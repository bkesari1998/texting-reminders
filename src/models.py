from db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from datetime import datetime

class Task(Base):
    DESCRIPTION_MAX_LEN = 255
    
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(DESCRIPTION_MAX_LEN))
    created_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    completed: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, description={self.description!r})"

    def __str__(self) -> str:
        return self.description
