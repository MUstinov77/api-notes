from typing import Any, Type, Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import session_provider
from app.models import Note, User
from app.notes.schemas import NoteQuery
from app.auth.router import check_user_is_authenticated

router = APIRouter(
    prefix='/notes',
    tags=['notes'],
)


@router.get('/')
async def get_my_notes(
        user: Annotated[User, Depends(check_user_is_authenticated)],
        session: Session = Depends(session_provider)):
    query = select(Note).join(User, User.id == Note.user_id)
    result = session.execute(query)

    return result.scalars().all()


@router.post('/')
async def create_note(note: NoteQuery, session: Session = Depends(session_provider)):
    note = note.model_dump()
    note = Note(**note)

    session.add(note)

    return note


@router.get('/{nickname}')
async def get_user_notes(nickname: str, session: Session = Depends(session_provider)):
    query = select(User).where(User.nickname == nickname)
    result = session.execute(query)
    user_id = result.scalars().one().id
    query = select(Note).where(Note.user_id == user_id)

    return result.scalars().all()

@router.get('/{note_id}')
async def get_note_by_id(note_id: int, session: Session = Depends(session_provider)):
    query = select(Note).where(Note.id == note_id)
    result = session.execute(query)
    return result.scalars().one()

