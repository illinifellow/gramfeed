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
