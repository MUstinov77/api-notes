from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import session_provider
from app.core.models import User

from .schemas import UserResponse

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get(
    '/',
    response_model=list[UserResponse]
)
def get_all_users(session: Session = Depends(session_provider)):
    query = select(User)
    result = session.execute(query)
    return result.scalars().all()


@router.get(
    '/{nickname}',
    response_model=UserResponse
)
def get_user_by_nickname(nickname: str, session: Session = Depends(session_provider)):
    query = select(User).where(User.nickname == nickname)
    result = session.execute(query)

    return result.scalars().one()

