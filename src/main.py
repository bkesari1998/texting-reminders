from typing import Annotated
from datetime import date, time
from pathlib import Path

from sqlalchemy.orm import Session

from fastapi import FastAPI, Form, Depends, Request, HTTPException
from fastapi.responses import Response, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from db import get_db
from api import TaskOut
from repository import TaskRepository

app = FastAPI()

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request,
         active_tab: str = "incomplete",
         db: Session = Depends(get_db)
) -> HTMLResponse:

    incomplete_tasks = TaskRepository.get_incomplete_tasks(db)
    completed_tasks = TaskRepository.get_completed_tasks(db)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "incomplete_tasks": incomplete_tasks,
            "completed_tasks": completed_tasks,
            "active_tab": active_tab
        },
    )

@app.post("/add-task")
def add_task(
    description: Annotated[str, Form()],
    deadline_date: Annotated[date | None, Form()] = None,
    deadline_time: Annotated[time | None, Form()] = None,
    active_tab_redirect: Annotated[str, Form()] = "incomplete",
    db: Session = Depends(get_db)
) -> RedirectResponse:
    try:
        # Validate description (basic validation since Form doesn't use Pydantic directly)
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        if len(description) > 255:
            raise ValueError("Description cannot exceed 255 characters")

        # Use repository to create task
        TaskRepository.create_task(
            db=db,
            description=description.strip(),
            deadline_date=deadline_date,
            deadline_time=deadline_time
        )

        return RedirectResponse(url=f"/?active_tab={active_tab_redirect}", status_code=303)
    except ValueError as e:
        # In a real app, you'd want to show this error to the user
        # For now, just redirect back with the error logged
        print(f"Validation error: {e}")
        return RedirectResponse(url=f"/?active_tab={active_tab_redirect}", status_code=303)

@app.patch("/toggle-completion/{task_id}", response_model=TaskOut)
def toggle_completion(
    task_id: int,
    db: Session = Depends(get_db)
) -> TaskOut:
    task = TaskRepository.toggle_task_completion(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

