from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.schemas import Token, UserQuery
from app.core.db import session_provider
from app.core.models import User
from app.core.utils import (
    authenticate_user,
    create_access_token,
    get_password_hash
    )


BASE_PREFIX = '/auth'
router = APIRouter(
    prefix=BASE_PREFIX,
    tags=['auth',]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=BASE_PREFIX + '/token',
)

@router.post('/signup')
async def signup(
        user_data: UserQuery,
        session: Session = Depends(session_provider)
):
    user_data = user_data.model_dump()
    hashed_password = get_password_hash(user_data.pop('password'))
    user = User(**user_data)
    user.hashed_password = hashed_password
    try:
        session.add(user)
    except Exception as e:
        print(e)
    return {'message': 'user created'}


@router.post('/token')
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(session_provider)
):
    user = authenticate_user(
        form_data.username,
        form_data.password,
        session
    )

    if not user:
        return {'message': 'invalid credentials'}

    token_timedelta = timedelta(minutes=20)
    access_token = create_access_token(
        data={'sub': user.nickname},
        expires_delta=token_timedelta,
    )
    return Token(access_token=access_token, token_type='bearer')
