import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import Message, RecipeDetailPublic, RecipeOverview
from test.utils.recipe import (
    add_multiple_random_recipes_to_db,
    add_random_recipe_to_db,
    create_random_recipe,
)


@pytest.mark.parametrize(("skip", "limit"), [(0, 5), (5, 10), (0, 100)])
def test_read_recipes(
    client: TestClient, session: Session, skip: int, limit: int
) -> None:
    count: int = 9
    expected_length = min(limit, count - skip)
    recipes = add_multiple_random_recipes_to_db(session=session, count=count)

    url = f"{settings.API_V1_STR}/recipes/"
    response = client.get(url, params={"skip": skip, "limit": limit})
    assert response.status_code == 200

    response_body = RecipeOverview(**response.json())
    assert response_body.count == len(recipes)
    assert len(response_body.data) == expected_length
    assert all(
        recipes[skip + i].id == response_body.data[i].id
        for i in range(expected_length)
    )


def test_create_recipe(client: TestClient) -> None:
    recipe = create_random_recipe()

    url = f"{settings.API_V1_STR}/recipes/"
    response = client.post(url, json=recipe.model_dump())
    assert response.status_code == 200

    response_body = RecipeDetailPublic(**response.json())

    # id is set by the server and therefore unknown before post request
    expected_response = RecipeDetailPublic.model_validate(
        recipe, update={"id": response_body.id}
    )
    assert response_body == expected_response


def test_read_recipe(client: TestClient, session: Session) -> None:
    recipe = add_random_recipe_to_db(session=session)
    expected_response = RecipeDetailPublic.model_validate(recipe)

    url = f"{settings.API_V1_STR}/recipes/{recipe.id}"
    response = client.get(url)
    assert response.status_code == 200

    response_body = RecipeDetailPublic(**response.json())
    assert response_body == expected_response


def test_read_recipe_not_found(client: TestClient) -> None:
    non_existent_id = "00000000-0000-0000-0000-000000000000"

    url = f"{settings.API_V1_STR}/recipes/{non_existent_id}"
    response = client.get(url)
    assert response.status_code == 404


def test_update_recipe(client: TestClient, session: Session) -> None:
    recipe = add_random_recipe_to_db(session=session)
    updated_recipe = create_random_recipe()

    url = f"{settings.API_V1_STR}/recipes/{recipe.id}"
    response = client.put(url, json=updated_recipe.model_dump())
    assert response.status_code == 200

    response_body = RecipeDetailPublic(**response.json())
    expected_response = RecipeDetailPublic.model_validate(
        updated_recipe, update={"id": recipe.id}
    )
    assert response_body == expected_response


def test_delete_recipe(client: TestClient, session: Session) -> None:
    recipe = add_random_recipe_to_db(session=session)

    url = f"{settings.API_V1_STR}/recipes/{recipe.id}"
    response = client.delete(url)
    assert response.status_code == 200

    response_body = Message(**response.json())
    expected_response = Message(message="Recipe deleted successfully")
    assert response_body == expected_response

    # Verify that the recipe is actually deleted
    get_response = client.get(url)
    assert get_response.status_code == 404
