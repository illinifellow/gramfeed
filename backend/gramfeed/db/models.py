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
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    posts: Mapped[list["Post"]] = relationship(back_populates="account", order_by="Post.taken_at.desc()")


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("account_id", "shortcode"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), index=True)
    shortcode: Mapped[str] = mapped_column(String(20))
    taken_at: Mapped[datetime] = mapped_column(index=True)
    caption: Mapped[str | None] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(String(10))  # image | video | carousel
    location: Mapped[str | None] = mapped_column(String(200))
    account: Mapped[Account] = relationship(back_populates="posts")
    media: Mapped[list["Media"]] = relationship(order_by="Media.position", cascade="all, delete-orphan")