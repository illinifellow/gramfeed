"""RQ jobs. The worker runs these synchronously, one account at a time, spaced out: Instagram
rate-limits by IP, and a burst of forty profiles is what gets a server blocked."""

import asyncio
from datetime import UTC, datetime

from redis import Redis
from rq import Queue, Retry
from sqlalchemy import select

from gramfeed.db.models import Account, Media, Post
from gramfeed.db.session import Session
from gramfeed.fetch.instagram import AccountUnavailable, fetch_profile, loader
from gramfeed.fetch.media import rehost
from gramfeed.settings import settings

queue = Queue("fetch", connection=Redis.from_url(settings().redis_url))


def enqueue_refresh(username: str) -> None:
    queue.enqueue(refresh, username, job_id=f"refresh:{username}", retry=Retry(max=3, interval=[300, 900, 3600]))


def refresh(username: str) -> int:
    return asyncio.run(_refresh(username))


async def _refresh(username: str) -> int:
    async with Session() as s:
        account = (await s.execute(select(Account).where(Account.username == username))).scalar_one()
        newest = (
            await s.execute(select(Post.taken_at).where(Post.account_id == account.id).order_by(Post.taken_at.desc()).limit(1))
        ).scalar()
        try:
            profile = fetch_profile(loader(settings().instagram_session_user), username, newest, settings().max_posts_per_feed)
        except AccountUnavailable as e:
            account.paused, account.last_error = True, str(e)
            await s.commit()
            return 0

        account.full_name, account.biography = profile.full_name, profile.biography
        account.avatar_key = rehost(profile.avatar_url, f"{username}/avatar")
        for p in profile.posts:
            post = Post(shortcode=p.shortcode, taken_at=p.taken_at, caption=p.caption, kind=p.kind, location=p.location)
            post.media = [
                Media(position=i, kind=m.kind, key=rehost(m.url, f"{username}/{p.shortcode}"), width=m.width, height=m.height)
                for i, m in enumerate(p.media)
            ]
            account.posts.append(post)
        account.last_fetched_at, account.last_error = datetime.now(UTC), None
        await s.commit()
        return len(profile.posts)


def schedule_all() -> None:
    """Called by the clock process: queue every active account, spread across the refresh interval."""
    async def usernames() -> list[str]:
        async with Session() as s:
            return list((await s.execute(select(Account.username).where(Account.paused.is_(False)))).scalars())

    names = asyncio.run(usernames())
    spacing = settings().refresh_minutes * 60 / max(1, len(names))
    for i, name in enumerate(names):