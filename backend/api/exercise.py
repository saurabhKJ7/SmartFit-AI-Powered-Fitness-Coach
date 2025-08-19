from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.exercise import Nutrition


from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from backend.model.exercise import Exercise


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/exercise/", response_model=Exercise)
def create_exercise(hero: Exercise, session: SessionDep):
    db_exercise= Exercise.model_validate(hero)
    session.add(db_exercise)
    session.commit()
    session.refresh(db_exercise)
    return db_nutrition


@app.get("/exercise/", response_model=list[Exercise])
def read_exercise(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/exercise/{exercise_id}", response_model=Exercise)
def read_exercise(exercise_id: int, session: SessionDep):
    hero = session.get(Exercise, exercise_id)
    if not hero:
        raise HTTPException(status_code=404, detail="exercise not found")
    return hero


@app.patch("/exercise/{exercise_id}", response_model=Exercise)
def update_nutrition(exercise_id: int, hero: Exercise, session: SessionDep):
    hero_db = session.get(Exercise, exercise_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="exercise not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

@app.delete("/exercise/{exercise_id}")
def delete_nutrition(exercise_id: int, session: SessionDep):
    hero = session.get(Exercise, exercise_id)
    if not hero:
        raise HTTPException(status_code=404, detail="exericise not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}