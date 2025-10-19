from sqlmodel import Session

from app.models import Recipe, RecipeCreate


def create_recipe(session: Session, recipe_in: RecipeCreate) -> Recipe:
    recipe = Recipe.model_validate(recipe_in)
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe
