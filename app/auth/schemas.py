from datetime import date

from pydantic import BaseModel


class UserQuery(BaseModel):
    nickname: str
    email: str
    password: str
    date_of_birth: date