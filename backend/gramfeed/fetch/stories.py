"""Stories fetcher.

Stories disappear after 24 hours, so every media URL is copied to our bucket before the caller
stores anything. This module is not wired into the refresh job yet.
"""

from dataclasses import dataclass
from datetime import UTC, datetime
from itertools import chain
from typing import Iterable

import instaloader

from gramfeed.fetch.instagram import AccountUnavailable
from gramfeed.fetch.media import rehost


@dataclass
class FetchedStoryMedia:
    kind: str
    key: str
    width: int | None
    height: int | None


@dataclass
class FetchedStory:
    media_id: str
    taken_at: datetime
    expires_at: datetime
    media: FetchedStoryMedia
    caption: str | None = None


def _dims(node: dict) -> tuple[int | None, int | None]:
    dims = node.get("dimensions") or {}
    return dims.get("width"), dims.get("height")
