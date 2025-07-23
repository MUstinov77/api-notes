from datetime import date

from pydantic import BaseModel

from app.core.models import User, Friend


class UserResponse(BaseModel):
    nickname: str
    email: str
    date_of_birth: date


