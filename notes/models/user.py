from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


from notes.core.base import Base


class User(Base):

    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(30))
