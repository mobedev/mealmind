from typing import Any

from fastapi import APIRouter
from sqlmodel import func, select

from app.core.db import SessionDep
from app.models import Recipe, RecipeOverview

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=RecipeOverview)
def read_recipes(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(Recipe)
    count = session.exec(count_statement).one()
    statement = select(Recipe).offset(skip).limit(limit)
    recipes = session.exec(statement).all()
    return RecipeOverview(data=recipes, count=count)
