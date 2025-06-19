from typing import Generator, Any

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine(
    'sqlite://',
    echo=False
)

def get_session() -> Generator[Session, Any, None]:

    engine = create_engine('sqlite://', echo=False)
    with Session(engine) as session:
        yield session

