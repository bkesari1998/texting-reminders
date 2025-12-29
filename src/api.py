from pydantic import BaseModel
from datetime import datetime, date, time

class TaskOut(BaseModel):
    id: int
    description: str
    created_datetime: datetime
    deadline_date: date | None = None
    deadline_time: time | None = None
    completed: bool = False

    model_config = {"from_attributes": True}