from typing import Annotated

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.params import Param, Depends
from sqlalchemy.orm import Session

from notes.models.models import User
from notes.core.db import get_session

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@auth_router.post('/signup')
async def sign_up(nickname: str, session: Annotated[Session, Depends(get_session)]):
    user = User(
        nickname=nickname,
    )
    session.commit()
    return user




@auth_router.get('/signin')
async def login():
    return ...