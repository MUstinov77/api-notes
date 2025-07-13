from datetime import date

from sqlalchemy import ForeignKey, String, Boolean
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


class Note(Base):

    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), default=1)
    user = relationship('User', back_populates='note')
    content: Mapped[str] = mapped_column(String(100))
