from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Account(Base):
    """A public Instagram account someone subscribed to."""
