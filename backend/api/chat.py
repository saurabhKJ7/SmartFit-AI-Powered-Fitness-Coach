from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.exercise import Nutrition


from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from backend.services.chat import Chat




app = FastAPI()

@app.post("/chat/ask/{userquery}", response_model=str)
def create_exercise(hero: userquery, session: SessionDep):
    response =Chat.chat_with_llm(userquery)
    return response


@app.get("/history/", response_model=list[Exercise])
def read_exercise(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


