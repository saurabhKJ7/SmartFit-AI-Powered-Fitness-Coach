from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.exercise import Nutrition


from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from backend.model.progresstracking import Progress


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


@app.post("/progress/", response_model=Progress)
def create_exercise(hero: Progress, session: SessionDep):
    db_progress= Progress.model_validate(hero)
    session.add(db_progress)
    session.commit()
    session.refresh(db_progress)
    return db_progress


@app.get("/progress/", response_model=list[Progress])
def read_progress(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/exercise/{progress_id}", response_model=Progress)
def read_progress(progress_id: int, session: SessionDep):
    hero = session.get(Progress, progress_id)
    if not hero:
        raise HTTPException(status_code=404, detail="progress tracking  not found")
    return hero


@app.patch("/progress/{progress_id}", response_model=Progress)
def update_progress(progress_id: int, hero: Progress, session: SessionDep):
    hero_db = session.get(Progress, progress_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="progress not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

@app.delete("/exercise/{progress_id}")
def delete_nutrition(progress_id: int, session: SessionDep):
    hero = session.get(Progress, progress_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Progress not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}