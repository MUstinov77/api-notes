from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.core.db import session_provider
from app.core.models import Note, User
from app.core.utils import get_current_user, get_note_by_field
from app.notes.schemas import NoteQuery

router = APIRouter(
    prefix='/notes',
    tags=['notes'],
)


@router.get(
    '/',
    response_model=list[NoteQuery]
)
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


@router.get(
    '/{note_id}',
    response_model=NoteQuery
)
async def get_note_by_id(
        note_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(session_provider)
):
    query = (
        select(Note).
        where(Note.id == note_id).
        join(User, user.id == Note.user_id)
    )
    result = session.execute(query)
    return result.scalars().first()

@router.delete(
    '/{note_id}'
)
async def delete_note_by_id(
        note_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(session_provider)
):
    session.execute(
        delete(Note).where(Note.id == note_id)
    )
    return {'message': 'note deleted'}