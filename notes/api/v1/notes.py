from fastapi import APIRouter, Request
from fastapi.params import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from notes.models import Note, User
from notes.db import session_provider



router = APIRouter(
    prefix='/notes',
    tags=['notes'],
)


@router.get('/')
def get_my_notes(session: Session = Depends(session_provider)):
    query = select(Note).join(User, User.id == Note.user_id)
    result = session.execute(query)

    return result.scalars().all()


@router.post('/{content}')
def create_note(request: Request, content: str, session: Session = Depends(session_provider)):
    note = Note(content=content)

    session.add(note)

    return note