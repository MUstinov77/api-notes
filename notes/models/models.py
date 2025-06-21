from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
    )

from notes.core.base import Base


class User(Base):

    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(30))
    note = relationship(
        'Note',
        back_populates='user',
    )


class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(300))
    user = relationship(
        'User',
        back_populates='note',
    )
