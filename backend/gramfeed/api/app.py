from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from gramfeed.db.models import Account, Post
from gramfeed.db.session import session
from gramfeed.feeds.render import build
from gramfeed.fetch.jobs import enqueue_refresh
from gramfeed.settings import settings

app = FastAPI(title="gramfeed", version="0.8.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

Db = Annotated[AsyncSession, Depends(session)]


def admin(authorization: str = Header("")) -> None:
    if authorization != f"Bearer {settings().admin_token}":
        raise HTTPException(401, "admin token required")


class AccountIn(BaseModel):
    username: str = Field(pattern=r"^[A-Za-z0-9._]{1,30}$")


class AccountOut(BaseModel):
    username: str
    full_name: str | None
    posts: int
    last_fetched_at: datetime | None
    last_error: str | None
    paused: bool
    feed_url: str

