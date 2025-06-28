from fastapi import APIRouter, Request
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import session_provider
from app.models import Note, User

router = APIRouter(
    prefix='/notes',
    tags=['notes'],
)

class NoteQuery(BaseModel):
    content: str


@router.get('/')
def get_my_notes(session: Session = Depends(session_provider)):
    # query = select(Note).join(User, User.id == Note.user_id)
    query = select(Note)
    result = session.execute(query)

    return result.scalars().all()


@router.post('/')
def create_note(note: NoteQuery, session: Session = Depends(session_provider)):
    note = note.model_dump()
    note = Note(**note)

    session.add(note)

    return note


@router.get('/{note_id}')
def get_note_by_id(note_id: int, session: Session = Depends(session_provider)):
    query = select(Note).where(Note.id == note_id)
    result = session.execute(query)
    return result.scalars().one()


@router.get('/{user_nickname}')
def get_user_notes(user_nickname: str, session: Session = Depends(session_provider)):
    user = session.query(User).where(User.nickname == user_nickname).first()
    print(user)
    query = select(Note).join(User, User.id == user.id)
    result = session.execute(query)

    return result.scalars().all()