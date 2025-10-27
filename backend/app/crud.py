import uuid

from sqlmodel import Session, func, select

from app.exceptions import RecipeNotFoundException
from app.models import (
    Ingredient,
    Recipe,
    RecipeCreate,
    RecipeOverview,
    RecipeUpdate,
)


def transform_recipe_create_to_recipe(recipe_in: RecipeCreate) -> Recipe:
    ingredients = [
        Ingredient.model_validate(ingredient)
        for ingredient in recipe_in.ingredients
    ]
    recipe = Recipe.model_validate(
        recipe_in, update={"ingredients": ingredients}
    )
    return recipe


def create_recipe(session: Session, recipe_in: RecipeCreate) -> Recipe:
    recipe = transform_recipe_create_to_recipe(recipe_in)
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


def read_recipe(session: Session, recipe_id: uuid.UUID) -> Recipe | None:
    statement = select(Recipe).where(Recipe.id == recipe_id)
    result = session.exec(statement)
    return result.one_or_none()


def read_recipes(
    session: Session, skip: int = 0, limit: int = 100
) -> RecipeOverview:
    count_statement = select(func.count()).select_from(Recipe)
    count = session.exec(count_statement).one()
    statement = select(Recipe).offset(skip).limit(limit)
    recipes = session.exec(statement).all()
    return RecipeOverview(data=recipes, count=count)


def update_recipe(
    session: Session, recipe_id: uuid.UUID, recipe_in: RecipeUpdate
) -> Recipe:
    recipe = read_recipe(session=session, recipe_id=recipe_id)
    if recipe is None:
        raise RecipeNotFoundException("Recipe not found")
    transformed_recipe_in = transform_recipe_create_to_recipe(recipe_in)
    update_dict = transformed_recipe_in.model_dump(exclude_unset=True)
    recipe.sqlmodel_update(update_dict)
    recipe.ingredients = transformed_recipe_in.ingredients
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


def delete_recipe(session: Session, recipe_id: uuid.UUID) -> None:
    recipe = read_recipe(session=session, recipe_id=recipe_id)
    if recipe is not None:
        session.delete(recipe)
        session.commit()
    else:
        raise RecipeNotFoundException("Recipe not found")
