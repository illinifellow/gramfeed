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


@app.get("/{username}.{fmt}", response_class=Response)
async def feed(username: str, fmt: str, db: Db) -> Response:
    if fmt not in ("rss", "atom", "xml"):
        raise HTTPException(404)
    account = (
        await db.execute(
            select(Account).where(Account.username == username.lower()).options(selectinload(Account.posts).selectinload(Post.media))
        )
    ).scalar_one_or_none()
    if account is None:
        raise HTTPException(404, f"@{username} is not followed here; add it in the admin")
    body = build(account, "atom" if fmt == "atom" else "rss")
    media = "application/atom+xml" if fmt == "atom" else "application/rss+xml"
    return Response(body, media_type=f"{media}; charset=utf-8", headers={"Cache-Control": "public, max-age=900"})


@app.get("/api/accounts", dependencies=[Depends(admin)])
async def accounts(db: Db) -> list[AccountOut]:
    rows = await db.execute(
        select(Account, func.count(Post.id)).outerjoin(Post).group_by(Account.id).order_by(Account.username)
    )
    return [
        AccountOut(
            username=a.username, full_name=a.full_name, posts=n, last_fetched_at=a.last_fetched_at,
            last_error=a.last_error, paused=a.paused, feed_url=f"{settings().public_url}/{a.username}.rss",
        )
        for a, n in rows.all()
    ]
