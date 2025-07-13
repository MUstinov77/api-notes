from datetime import date

from pydantic import BaseModel


class UserResponse(BaseModel):
    nickname: str
    email: str
    date_of_birth: date
