from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    description: str
    deadline: datetime | None = None

class TaskOut(BaseModel):
    id: int
    description: str
    deadline: datetime | None = None

    model_config = {"from_attributes": True}