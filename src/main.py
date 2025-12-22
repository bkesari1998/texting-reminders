from task import Task
from db import TaskDatabase

from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "hello"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)
