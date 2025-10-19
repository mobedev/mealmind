import random
import string

from sqlmodel import Session

from app import crud
from app.models import Ingredient, Recipe, RecipeCreate, Unit


def create_random_string(length: int) -> str:
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=length)
    )


def create_random_ingredients(amount: int) -> list[Ingredient]:
    ingredients = []
    for _ in range(amount):
        ingredient = Ingredient(
            name=create_random_string(5),
            quantity=random.randint(1, 100),
            unit=random.choice(list(Unit)),
        )
        ingredients.append(ingredient)
    return ingredients


def create_random_recipe(session: Session) -> Recipe:
    recipe_in = RecipeCreate(
        title=create_random_string(10),
        description=create_random_string(20),
        summary=create_random_string(30),
        ingredients=create_random_ingredients(5),
    )
    return crud.create_recipe(session=session, recipe_in=recipe_in)
