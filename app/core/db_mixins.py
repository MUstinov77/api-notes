from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column


class UserMixin:

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(
        String(30),
        unique=True
    )
    email: Mapped[str] = mapped_column(String())
    date_of_birth: Mapped[date] = mapped_column(
        Date()
    )
