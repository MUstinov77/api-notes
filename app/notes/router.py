from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import session_provider
from app.core.models import Note, User
from app.core.utils import get_current_user
from app.notes.schemas import NoteQuery

router = APIRouter(
    prefix='/notes',
    tags=['notes'],
)


@router.get(
    '/',
    response_model=list[NoteQuery])
async def get_my_notes(
        user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(session_provider)
):
    query = select(Note).where(Note.user_id == user.id).join(User, User.id == Note.user_id)
    result = session.execute(query)
    return result.scalars().all()


@router.post('/')
async def create_note(
        note: NoteQuery,
        user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(session_provider)
):
    note = note.model_dump()
    note['user_id'] = user.id
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

