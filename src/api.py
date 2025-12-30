from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date, time


class TaskCreate(BaseModel):
    """Schema for creating a new task with validation."""
    description: str = Field(..., min_length=1, max_length=255)
    deadline_date: date | None = None
    deadline_time: time | None = None

    @field_validator('description')
    @classmethod
    def description_not_empty(cls, v: str) -> str:
        """Validate that description is not empty or whitespace only."""
        if not v.strip():
            raise ValueError('Description cannot be empty or whitespace only')
        return v.strip()


class TaskOut(BaseModel):
    """Schema for returning task data."""
    id: int
    description: str
    created_datetime: datetime
    deadline_date: date | None = None
    deadline_time: time | None = None
    completed: bool = False

    model_config = {"from_attributes": True}