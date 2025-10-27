import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.core.db import SessionDep
from app.exceptions import RecipeNotFoundException
from app.models import (
    Message,
    RecipeCreate,
    RecipeDetailPublic,
    RecipeOverview,
    RecipeUpdate,
)

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=RecipeOverview)
def read_recipes(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    return crud.read_recipes(session=session, skip=skip, limit=limit)


@router.post("/", response_model=RecipeDetailPublic)
def create_recipe(session: SessionDep, recipe_in: RecipeCreate) -> Any:
    return crud.create_recipe(session=session, recipe_in=recipe_in)


@router.get("/{id}", response_model=RecipeDetailPublic)
def read_recipe(session: SessionDep, id: uuid.UUID) -> Any:
    recipe = crud.read_recipe(session=session, recipe_id=id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/{id}", response_model=RecipeDetailPublic)
def update_recipe(
    session: SessionDep, id: uuid.UUID, recipe_in: RecipeUpdate
) -> Any:
    try:
        return crud.update_recipe(
            session=session, recipe_id=id, recipe_in=recipe_in
        )
    except RecipeNotFoundException:
        raise HTTPException(status_code=404, detail="Recipe not found")


@router.delete("/{id}", response_model=Message)
def delete_recipe(session: SessionDep, id: uuid.UUID) -> Any:
    try:
        crud.delete_recipe(session=session, recipe_id=id)
    except RecipeNotFoundException:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return Message(message="Recipe deleted successfully")
