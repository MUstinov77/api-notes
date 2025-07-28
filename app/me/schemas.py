from datetime import date
from pydantic import BaseModel

from app.notes.schemas import NoteQuery
from app.users.schemas import UserResponse


class MeResponse(BaseModel):
    nickname: str
    email: str
    date_of_birth: date

    notes: list[NoteQuery]
