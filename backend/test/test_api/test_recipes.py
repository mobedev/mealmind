from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from test.utils.recipe import create_random_recipe


def test_read_recipe(client: TestClient, session: Session) -> None:
    recipe = create_random_recipe(session=session)
    url = f"{settings.API_V1_STR}/recipes/{recipe.id}"
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == recipe.title
    assert data["description"] == recipe.description
    assert data["summary"] == recipe.summary
    assert len(data["ingredients"]) == len(recipe.ingredients)
