import uuid
from enum import StrEnum
from typing import Sequence

from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel import Enum as SQLEnum


class Unit(StrEnum):
    gram = "gram"
    ml = "ml"
    piece = "piece"


class RecipeBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    summary: str | None = Field(default=None, max_length=500)


class RecipeWithUid(RecipeBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class Recipe(RecipeWithUid, table=True):
    ingredients: list["Ingredient"] = Relationship(
        back_populates="recipe", cascade_delete=True
    )


class RecipeDetailPublic(RecipeWithUid):
    ingredients: list["IngredientPublic"] = Field(default_factory=list)


class RecipeCreate(RecipeBase):
    ingredients: list["IngredientPublic"] = Field(default_factory=list)


class RecipeUpdate(RecipeCreate):
    pass


class IngredientBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    unit: Unit = Field(sa_column=Column(SQLEnum(Unit), default=Unit.piece))


class Ingredient(IngredientBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    recipe_id: uuid.UUID | None = Field(default=None, foreign_key="recipe.id")
    recipe: Recipe = Relationship(back_populates="ingredients")


class IngredientPublic(IngredientBase):
    pass


class RecipeOverview(SQLModel):
    data: Sequence[RecipeWithUid]
    count: int


class Message(SQLModel):
    message: str
