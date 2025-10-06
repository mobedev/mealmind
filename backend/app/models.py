import uuid
from typing import Sequence

from sqlmodel import Field, SQLModel


class RecipeBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class Recipe(RecipeBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class RecipeOverview(SQLModel):
    data: Sequence[Recipe]
    count: int
