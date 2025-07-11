from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from app.auth.schemas import Token, UserQuery, TokenData
from app.db import session_provider
from app.models import User

BASE_PREFIX = '/auth'
router = APIRouter(
    prefix=BASE_PREFIX,
    tags=['auth',]
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=BASE_PREFIX + '/token'
)


@router.post("/signup")
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

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_from_db(
        username: str,
        session: Session = Depends(session_provider)
):
    query = select(User).where(User.nickname == username)
    result = session.execute(query)
    return result.scalars().one()

def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=20)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, 'secret', 'HS256')
    return encoded_jwt

def check_user_is_authenticated(
        token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        nickname = payload.get('sub')
        if not nickname:
            raise credentials_exception
        token_data = TokenData(nickname=nickname)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_from_db(token_data.nickname)
    if not user:
        raise credentials_exception
    return user






@router.post('/token')
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = get_user_from_db(form_data.username)

    if not user:
        return {'message': 'invalid credentials'}

    if not verify_password(form_data.password, user.hashed_password):
        return {'message': 'wrong password'}
    token_timedelta = timedelta(minutes=20)
    access_token = create_access_token(
        data={'sub': user.nickname},
        expires_delta=token_timedelta
    )
    return Token(access_token=access_token, token_type='bearer')




