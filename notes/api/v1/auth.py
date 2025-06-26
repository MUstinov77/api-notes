from fastapi import APIRouter
from fastapi.params import Depends

from sqlalchemy.orm import Session

from notes.models import User
from notes.db import session_provider


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.get('/signup')
def signup(nickname: str, session: Session = Depends(session_provider)):
    user = User(nickname=nickname)
    session.add(user)

    return user

