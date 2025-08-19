from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.exercise import Nutrition


from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from backend.api.exercise import Nutrition



# class UserBase(SQLModel):
#     username: str = Field(default=None)
#     email: str | None = Field(default=None)
#     age: int | None = Field(default=None)
#     weight: int | None = Field(default=None)
#     height: int | None = Field(default=None)
#     goals: str | None = Field(default=None)



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


@app.post("/nutrition/", response_model=Nutrition)
def create_users(hero: Nutrition, session: SessionDep):
    db_nutrition= Nutrition.model_validate(hero)
    session.add(db_nutrition)
    session.commit()
    session.refresh(db_nutrition)
    return db_nutrition


@app.get("/nutrition/", response_model=list[Nutrition])
def read_nutrition(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/nutrition/{nutrition_id}", response_model=Nutrition)
def read_nutrition(nutrition_id: int, session: SessionDep):
    hero = session.get(Nutrition, nutrition_id)
    if not hero:
        raise HTTPException(status_code=404, detail="nutrition not found")
    return hero


@app.patch("/nutritipon/{nutrition_id}", response_model=Nutrition)
def update_nutrition(nutrition_id: int, hero: Nutrition, session: SessionDep):
    hero_db = session.get(Nutrition, nutrition_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="nutrition not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

@app.delete("/nutrition/{nutrition_id}")
def delete_nutrition(nutrition_id: int, session: SessionDep):
    hero = session.get(Nutrition, nutrition_id)
    if not hero:
        raise HTTPException(status_code=404, detail="nutrition not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}