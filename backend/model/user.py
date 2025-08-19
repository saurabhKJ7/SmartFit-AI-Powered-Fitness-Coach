from sqlmodel import Field, SQLModel

#username email age weigth height goal 
class user(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(default=None)
    email: str | None = Field(default=None)
    age: int | None = Field(default=None)
    weight: int | None = Field(default=None)
    height: int | None = Field(default=None)
    goals: str | None = Field(default=None)
