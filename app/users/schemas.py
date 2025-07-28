from datetime import date

from pydantic import BaseModel

from app.core.models import Friend, User


class UserResponse(BaseModel):
    nickname: str
    email: str
    date_of_birth: date
