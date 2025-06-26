from fastapi.params import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from notes.models import Base


engine = create_engine('sqlite:///notes.db')


def create_session():
    with Session(engine) as session:

        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

def session_provider(session: Session = Depends(create_session)):
    return session

def init_db():
    Base.metadata.create_all(engine)
