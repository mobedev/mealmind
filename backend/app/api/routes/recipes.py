import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.core.db import SessionDep
from app.models import Recipe, RecipeDetailPublic, RecipeOverview

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=RecipeOverview)
def read_recipes(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(Recipe)
    count = session.exec(count_statement).one()
    statement = select(Recipe).offset(skip).limit(limit)
    recipes = session.exec(statement).all()
    return RecipeOverview(data=recipes, count=count)


@router.get("/{id}", response_model=RecipeDetailPublic)
def read_recipe(session: SessionDep, id: uuid.UUID) -> Any:
    statement = select(Recipe).where(Recipe.id == id)
    result = session.exec(statement)
    recipe = result.one_or_none()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
