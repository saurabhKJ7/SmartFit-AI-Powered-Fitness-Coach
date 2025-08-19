from sqlmodel import Field, SQLModel

#user_id, date, meals, calories, macronutrients (protein, carbs, fats)
class Nutrition(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: str
    meal: str
    calories: int 
    macronutrients: str 
