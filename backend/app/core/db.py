from collections.abc import Generator
from typing import Annotated
from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings
from fastapi import Depends

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)


def init_db(session: Session) -> None:
    # TODO: replace this with Alembic migrations
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
