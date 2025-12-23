from task import Task
from db import TaskDatabase

from fastapi import FastAPI, Form
from fastapi.responses import Response

from twilio.twiml.messaging_response import MessagingResponse
from contextlib import asynccontextmanager

db = TaskDatabase("tasks.db")
db.connect()
db.create_tasks_table()

app = FastAPI()

@app.post("/sms")
def sms_handler(Body: str = Form(...)):
    resp = MessagingResponse()
    
    if Body.startswith("Remind me to"):
        db.add_task(Task(Body[len("Remind me to"):]))
        msg = resp.message("Ok, I'll remind you to do that!'")
    else:
        msg = resp.message("Sorry, I didn't understand that :(")

    return str(resp)
    

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

