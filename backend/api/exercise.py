from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/exercise")
def getAllWorkout():
    return ""


@app.post("/exercise")
def saveWorkout():
    return ""


@app.put("/exercise")
def updateWorkout():
    return ""

@app.delete("/exercise")
def deleteWorkout():
    return ""