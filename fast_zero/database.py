from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import Settings


settings = Settings()
engine = create_engine(settings.DATABASE_URL)


def get_session() -> Generator[Session, None, None]:
    """Create a new SQLAlchemy session."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
