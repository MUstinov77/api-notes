from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.models import User, Friend
from app.users.schemas import UserResponse
from app.core.utils import get_current_user

from app.core.db import session_provider

router = APIRouter(
    prefix='/me',
    tags=['me'],
)


@router.get(
    '/',
    response_model=UserResponse
)
async def get_me(
        user: Annotated[User, Depends(get_current_user)],
):
    return user


@router.get(
    '/friends',
    response_model=list[UserResponse]
)
async def get_my_friends(
        user: Annotated[User, Depends(get_current_user)]
):
    return user.friends


@router.delete(
    '/friends/{nickname}'
)
async def delete_friend(
        nickname: str,
        user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(session_provider)
):
    query = (
        select(Friend).where(
            Friend.nickname == nickname and Friend.user_id == user.id).
        join(User, user.id == Friend.user_id)
    )
    result = session.execute(query)
    session.delete(result.scalars().first())
    return {'message': 'friend deleted'}