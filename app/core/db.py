from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.models import Base

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

def destroy_db():
    Base.metadata.drop_all(engine)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        init_db()
        yield
    finally:
        #destroy_db()
        return


