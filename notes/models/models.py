from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
    )

from ..core.base import Base


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
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user_account.id'),
        index=True
    )
    user = relationship(
        'User',
        back_populates='note',
    )
