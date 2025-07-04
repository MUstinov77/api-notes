from hashlib import sha256

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.schemas import UserQuery
from app.db import session_provider
from app.models import User

BASE_PREFIX = '/auth'
router = APIRouter(
    prefix=BASE_PREFIX,
    tags=['auth',]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=BASE_PREFIX)


@router.post("/signup")
async def signup(
        user_data: UserQuery,
        session: Session = Depends(session_provider)
):
    user_data = user_data.model_dump()
    hashed_password = sha256(user_data.get('password')).hexdigest()
    print(hashed_password)
    user = User(**user_data)
    user.hashed_password = hashed_password
    try:
        session.add(user)
    except Exception as e:
        print(e)
    return {'message': 'user created'}

