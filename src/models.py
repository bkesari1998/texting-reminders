from db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Task(Base):
    DESCRIPTION_MAX_LEN = 255
    
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(DESCRIPTION_MAX_LEN))

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, description={self.description!r})"

    def __str__(self) -> str:
        return self.description