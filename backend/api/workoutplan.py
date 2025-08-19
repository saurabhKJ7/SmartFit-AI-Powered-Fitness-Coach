from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.exercise import Nutrition


from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from backend.model.workoutModel import workout


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


@app.post("/workout/", response_model=workout)
def create_workout(hero: workout, session: SessionDep):
    db_workout= workout.model_validate(hero)
    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)
    return db_workout


@app.get("/workout/", response_model=list[workout])
def read_workout(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    workout = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return workout


@app.get("/workout/{workout_id}", response_model=workout)
def read_workout(workout_id_id: int, session: SessionDep):
    hero = session.get(workout, workout_id)
    if not hero:
        raise HTTPException(status_code=404, detail="workout plan not found")
    return hero


@app.patch("/workout/{workout_id}", response_model=workout)
def update_workout(workout_id: int, hero: workout, session: SessionDep):
    hero_db = session.get(workout, workout_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="workout plan not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

@app.delete("/workout/{workout_id}")
def delete_workout(workout_id: int, session: SessionDep):
    hero = session.get(workout, workout_id)
    if not hero:
        raise HTTPException(status_code=404, detail="workout not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}