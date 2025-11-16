from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Account(Base):
    """A public Instagram account someone subscribed to."""

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(150))
    biography: Mapped[str | None] = mapped_column(Text)
    avatar_key: Mapped[str | None] = mapped_column(String(200))
    last_fetched_at: Mapped[datetime | None]
    last_error: Mapped[str | None] = mapped_column(Text)
    # a private or deleted account stops being polled until someone retries it
    paused: Mapped[bool] = mapped_column(default=False)