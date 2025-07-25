from datetime import date

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String())
    hashed_password: Mapped[str] = mapped_column()
    date_of_birth: Mapped[date] = mapped_column()
    note = relationship('Note', back_populates='user', cascade='all, delete-orphan')
    disabled: Mapped[bool] = mapped_column(Boolean(), default=True)

    friends = relationship(
        'Friend',
        foreign_keys='Friend.friend_id',
        back_populates='user'
    )


class Note(Base):

    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='note')
    content: Mapped[str] = mapped_column(String(100))


class Friend(Base):

    __tablename__ = 'friends'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    friend_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='friends'
    )
