from typing import Annotated
from datetime import datetime
from os import environ

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session

from fastapi import FastAPI, Form, Depends
from fastapi.responses import Response, HTMLResponse

from db import engine
from models import Task
from api import TaskOut

from typing import Generator

SessionLocal = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    with open(environ["TEXTING_REMINDERS_INDEX_PATH"]) as f:
        return f.read()

@app.post("/add-task", response_model=TaskOut, status_code=201)
def add_task(
    description: Annotated[str, Form()],
    deadline: Annotated[datetime | None, Form()] = None,
    db: Session = Depends(get_db)
) -> TaskOut:
    
    task = Task(description=description, deadline=deadline)
    db.add(task)
    db.commit()
    db.refresh(task)

    return task

@app.get("/all-tasks", response_model=list[TaskOut])
def get_all_tasks(db: Session = Depends(get_db)) -> list[TaskOut]:
    stmt = select(Task)
    result = db.execute(stmt)
    tasks = result.scalars().all()

    return tasks
    
@app.get("/task", response_model=TaskOut)
def get_task(
    id: int, 
    db: Session = Depends(get_db)
) -> TaskOut | Response:
    stmt = select(Task).where(Task.id == id)
    result = db.execute(stmt)
    task = result.scalar_one_or_none()

    if task:
        return task
    else:
        return Response(status_code=404)

@app.patch("/toggle-completion/{task-id}", response_model=TaskOut)
def toggle_completion(
    id: int,
    db: Session = Depends(get_db)
) -> TaskOut:
    
    stmt = select(Task).where(Task.id == id)
    result = db.execute(stmt)
    task = result.scalar_one_or_none()

    if task:
        task.completed = not task.completed
        db.commit()
        db.refresh(task)
        return task
    else:
        return Response(status_code=404)

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

