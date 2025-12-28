from pydantic import BaseModel
from datetime import datetime

class TaskOut(BaseModel):
    id: int
    description: str
    created_datetime: datetime
    deadline: datetime | None = None
    completed: bool = False

    model_config = {"from_attributes": True}