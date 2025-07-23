from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import session_provider
from app.core.models import User, Friend
from app.core.utils import get_current_user, get_user_from_db

from .schemas import UserResponse

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get(
    '/',
    response_model=list[UserResponse]
)
async def get_all_users(session: Session = Depends(session_provider)):
    query = select(User)
    result = session.execute(query)
    return result.scalars().all()


@router.get(
    '/{nickname}',
    response_model=UserResponse
)
async def get_user_by_nickname(
        nickname: str,
        session: Session = Depends(session_provider)
):
    query = select(User).where(User.nickname == nickname)
    result = session.execute(query)

    return result.scalars().one()


@router.get(
    '/me/friends',
)
async def get_my_friends(
        user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(session_provider)
):
    query = select(Friend).where(Friend.user_id == user.id)
    result = session.execute(query)
    return result.scalars().all()


@router.post(
    '/{nickname}/add-friend'
)
async def add_friend(
        nickname: str,
        user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(session_provider)
):
    friend_to_add = get_user_from_db(nickname, session)
    if not friend_to_add:
        raise HTTPException(
            status_code=404,
            detail='user not found'
        )
    friend = Friend(
        user_id=user.id,
        friend_id=friend_to_add.id
    )
    session.add(friend)
    return {'message': 'friend added'}