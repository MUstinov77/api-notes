from fastapi import APIRouter, Request
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from typing import Any


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


@router.get('/{nickname}')
def get_user_notes(nickname: str, session: Session = Depends(session_provider)):
    query = select(User).where(User.nickname == nickname)
    result = session.execute(query)
    user_id = result.scalars().one().id
    query = select(Note).where(Note.user_id == user_id)

    return result.scalars().all()

@router.get('/{note_id}')
def get_note_by_id(note_id: int, session: Session = Depends(session_provider)):
    query = select(Note).where(Note.id == note_id)
    result = session.execute(query)
    return result.scalars().one()

def get_notes_by_field(field: Any, field_value: Any, session: Session = Depends(session_provider)):
    query = select(Note).where(field == field_value).returnning(Note)
