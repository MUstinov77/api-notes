from pydantic import BaseModel


class NoteQuery(BaseModel):
    content: str
