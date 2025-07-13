from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    )
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.schemas import Token, TokenData, UserQuery
from app.db import session_provider
from app.models import User

SECRET_KEY = '31302fb0fa15911d4b424e1ee164f6ff5a5c51a122b692f186c99f66c2088666'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

BASE_PREFIX = '/auth'
router = APIRouter(
    prefix=BASE_PREFIX,
    tags=['auth',]
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=BASE_PREFIX + '/token',
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
        session: Session
):
    query = select(User).where(User.nickname == username)
    result = session.execute(query)
    return result.scalars().one()

def authenticate_user(
        nickname: str,
        password: str,
        session: Session
):
    user = get_user_from_db(nickname, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

async def check_user_is_authenticated(
        token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nickname = payload.get('sub')
        if not nickname:
            raise credentials_exception
        token_scopes = payload.get('scopes', [])
        token_data = TokenData(scopes=token_scopes,nickname=nickname)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user_from_db(token_data.nickname)
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(check_user_is_authenticated)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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
