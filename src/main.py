from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session

from fastapi import FastAPI, Form, Depends
from fastapi.responses import Response

from twilio.twiml.messaging_response import MessagingResponse

from db import engine
from models import Task
from api import TaskCreate, TaskOut

from typing import Generator

SessionLocal = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/add-reminder", response_model=TaskOut, status_code=201)
def add_reminder(
    new_task: TaskCreate,
    db: Session = Depends(get_db)
) -> TaskOut:
    task = Task(description=new_task.description, deadline=new_task.deadline)
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
) -> TaskOut:
    stmt = select(Task).where(Task.id == id)
    result = db.execute(stmt)
    task = result.scalar_one_or_none()

    if task:
        return task
    else:
        return Response(status_code=404)

@app.post("/sms")
def sms_handler(Body: str = Form(...)):
    resp = MessagingResponse()
    
    with Session(engine) as session:
        if Body.startswith("Remind me to"):
            task = Task(description=Body[len("Remind me to"):])
            session.add(task)
            session.commit()
            resp.message("Ok, I will remind you to do that.")
        elif Body == "What are my tasks?":
            stmt = select(Task)
            result = session.execute(stmt)
            tasks = result.scalars().all()
            tasks_str = ""
            for task in tasks:
                tasks_str += str(task) + "\n\n"
            resp.message(tasks_str)
        else:
            msg = resp.message("Sorry, I didn't understand that :(")

        return Response(
            content=str(resp),
            media_type="application/xml"
        )
    

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

