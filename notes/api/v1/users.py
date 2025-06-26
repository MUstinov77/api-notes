from sqlalchemy import select
from sqlalchemy.orm import Session

from notes.models import User
from notes.db import session_provider
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/')
def get_all_users(session: Session = Depends(session_provider)):
    return session.query(User).all()


@router.get('/{nickname}')
def get_user_by_nickname(nickname: str, session: Session = Depends(session_provider)):
    query = select(User).where(User.nickname == nickname).join
    print(query)
    result = session.execute(query)

    return result.scalars().first()

