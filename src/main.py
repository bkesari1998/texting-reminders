from typing import Annotated
from datetime import date, time
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session

from fastapi import FastAPI, Form, Depends, Request
from fastapi.responses import Response, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from db import engine
from models import Task
from api import TaskOut

from typing import Generator

try:
    BASE_DIR = Path(__file__).resolve().parent.parent
except NameError:
    BASE_DIR = Path.cwd()

SessionLocal = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request,
         db: Session = Depends(get_db)
) -> HTMLResponse:
    
    stmt = select(Task)
    result = db.execute(stmt)
    tasks = result.scalars().all()

    incomplete_tasks = []
    completed_tasks = []

    for task in tasks:
        if task.completed:
            completed_tasks.append(task)
        else:
            incomplete_tasks.append(task)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "incomplete_tasks": incomplete_tasks,
            "completed_tasks": completed_tasks
        },
    )

@app.post("/add-task")
def add_task(
    description: Annotated[str, Form()],
    deadline_date: Annotated[date | None, Form()] = None,
    deadline_time: Annotated[time | None, Form()] = None,
    db: Session = Depends(get_db)
) -> RedirectResponse:
    
    if deadline_time and not deadline_date:
        deadline_date = date.today()

    task = Task(description=description, deadline_date=deadline_date, deadline_time=deadline_time)
    db.add(task)
    db.commit()

    return RedirectResponse(url="/", status_code=303)

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

@app.patch("/toggle-completion/{task_id}", response_model=TaskOut)
def toggle_completion(
    task_id: int,
    db: Session = Depends(get_db)
) -> TaskOut:
    
    stmt = select(Task).where(Task.id == task_id)
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

