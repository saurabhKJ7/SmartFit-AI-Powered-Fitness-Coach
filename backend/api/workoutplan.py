from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/workout")
def getAllWorkout():
    return ""


@app.post("/workout")
def saveWorkout():
    return ""


@app.put("/workout")
def updateWorkout():
    return ""

@app.delete("/workout")
def deleteWorkout():
    return ""