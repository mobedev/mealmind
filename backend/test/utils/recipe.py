import random
import string

from sqlmodel import Session

from app import crud
from app.models import IngredientPublic, Recipe, RecipeCreate, Unit


def create_random_string(length: int) -> str:
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=length)
    )


def create_random_ingredients(amount: int) -> list[IngredientPublic]:
    ingredients = []
    for _ in range(amount):
        ingredient = IngredientPublic(
            name=create_random_string(5),
            quantity=random.randint(1, 100),
            unit=random.choice(list(Unit)),
        )
        ingredients.append(ingredient)
    return ingredients


def create_random_recipe() -> RecipeCreate:
    return RecipeCreate(
        title=create_random_string(10),
        description=create_random_string(20),
        summary=create_random_string(30),
        ingredients=create_random_ingredients(5),
    )


def add_random_recipe_to_db(session: Session) -> Recipe:
    recipe_in = create_random_recipe()
    return crud.create_recipe(session=session, recipe_in=recipe_in)


def add_multiple_random_recipes_to_db(
    session: Session, count: int
) -> list[Recipe]:
    recipes: list[Recipe] = []
    for _ in range(count):
        recipe = add_random_recipe_to_db(session=session)
        recipes.append(recipe)
    return recipes
