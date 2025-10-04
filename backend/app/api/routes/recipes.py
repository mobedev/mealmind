from typing import Any

from fastapi import APIRouter
from app.models import Recipe

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=Recipe)
def read_recipes() -> Any:
    return Recipe(title="Sample Recipe", description="This is a sample recipe.")