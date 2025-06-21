from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import Session


engine = create_engine(
    'sqlite://',
    echo=False
)


def get_session() -> Generator[Session, Any, None]:
    engine = create_engine('sqlite://', echo=False)
    with Session(engine) as session:
        yield session
