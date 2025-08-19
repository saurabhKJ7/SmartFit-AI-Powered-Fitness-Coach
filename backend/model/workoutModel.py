from sqlmodel import Field, SQLModel

#plan_name, difficulty_level, duration, target_muscle_groups, exercises_list
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plan_name: str
    difficulty_level: str
    duration: int | None = None
    target_muscle_groups: str 
    exercises_list: str
