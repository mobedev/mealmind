from sqlmodel import SQLModel

class Recipe(SQLModel):
    title: str
    description: str | None = None