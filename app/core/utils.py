from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.schemas import Token, TokenData
from app.core.db import session_provider
from app.core.models import Note, User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token'
)

SECRET_KEY = '31302fb0fa15911d4b424e1ee164f6ff5a5c51a122b692f186c99f66c2088666'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_from_db(
        nickname: str,
        session: Session = Depends(session_provider)
):
    query = select(User).where(User.nickname == nickname)
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


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session = Depends(session_provider)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        nickname = payload.get('sub')
        if not nickname:
            raise credentials_exception
        token_data = TokenData(nickname=nickname)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user_from_db(token_data.nickname, session)
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(
        token: Token,
        session: Session
):
    current_user: User = get_current_user(token, session)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_note_by_field(
        field: str,
        field_value,
        session: Session = Depends(session_provider)
):
    query = (
        select(Note).where(field == field_value).
        join(User, User.id == Note.user_id)
    )
    result = session.execute(query)
    return result.scalars().first()
