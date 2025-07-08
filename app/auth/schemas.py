from datetime import date

from pydantic import BaseModel


class UserQuery(BaseModel):
    nickname: str
    email: str
    password: str
    date_of_birth: date


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    nickname: str
