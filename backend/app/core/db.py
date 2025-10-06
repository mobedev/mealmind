from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.models import Recipe

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)


def init_db(session: Session) -> None:
    # TODO: replace this with Alembic migrations
    SQLModel.metadata.create_all(engine)

    # write sample recipe
    sample_recipe = Recipe(
        title="Spaghetti Carbonara",
        description=(
            "A classic Italian pasta dish made with eggs, cheese, "
            "pancetta, and pepper."
        ),
    )
    session.add(sample_recipe)
    session.commit()


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
