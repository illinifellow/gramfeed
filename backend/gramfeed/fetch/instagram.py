"""Fetching from Instagram.

Why Python: instaloader is the maintained, battle-tested client for Instagram's public web
endpoints — it tracks their changing query hashes, handles sessions and backs off on 429s. There is
nothing comparable in the TypeScript ecosystem, and re-implementing it would mean chasing
Instagram's changes alone.
"""

from dataclasses import dataclass
from datetime import UTC, datetime
from itertools import islice

import instaloader


@dataclass
class FetchedMedia:
    kind: str
    url: str
    width: int | None
    height: int | None


@dataclass
class FetchedPost:
    shortcode: str
    taken_at: datetime
    caption: str | None
    kind: str