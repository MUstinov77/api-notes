from datetime import date

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base
from .db_mixins import UserMixin

class User(
    UserMixin,
    Base
):

    __tablename__ = 'users'

    hashed_password: Mapped[str] = mapped_column()
    note = relationship('Note', back_populates='user', cascade='all, delete-orphan')
    disabled: Mapped[bool] = mapped_column(Boolean(), default=True)

    friends = relationship(
        'Friend',
        foreign_keys='Friend.user_id',
        back_populates='user'
    )


class Note(Base):

    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='note')
    content: Mapped[str] = mapped_column(String(100))


class Friend(
    UserMixin,
    Base
):

    __tablename__ = 'friends'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    friend_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='friends'
    )