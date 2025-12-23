from task import Task
from db import TaskDatabase

from fastapi import FastAPI, Form
from fastapi.responses import Response

from twilio.twiml.messaging_response import MessagingResponse

db = TaskDatabase("tasks.db")
db.connect()
db.create_tasks_table()

app = FastAPI()

@app.post("/sms")
def sms_handler(Body: str = Form(...)):
    resp = MessagingResponse()
    
    if Body.startswith("Remind me to"):
        db.add_task(Task(Body[len("Remind me to"):]))
        msg = resp.message("Ok, I'll remind you to do that!")
    elif Body == "What are my tasks?":
        tasks = db.get_tasks()
        
        tasks_string = ""
        for task in tasks:
            tasks_string += (str(task) + "\n\n")

        msg = resp.message(tasks_string)
    else:
        msg = resp.message("Sorry, I didn't understand that :(")

    return Response(
        content=str(resp),
        media_type="application/xml"
    )
    

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

