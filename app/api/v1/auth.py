from datetime import datetime

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import session_provider
from app.models import User

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

class UserQuery(BaseModel):
    nickname: str
    email: str
    date_of_birth: datetime


@router.post('/signup')
def signup(user_data: UserQuery, session: Session = Depends(session_provider)):
    user_data = user_data.model_dump()
    user = User(**user_data)
    session.add(user)
    return user

