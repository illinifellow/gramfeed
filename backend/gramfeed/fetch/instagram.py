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
    location: str | None
    media: list[FetchedMedia]


@dataclass
class FetchedProfile:
    username: str
    full_name: str | None
    biography: str | None
    avatar_url: str
    private: bool
    posts: list[FetchedPost]


class AccountUnavailable(Exception):
    """Private, renamed or deleted: polling stops until someone retries."""


def loader(session_user: str | None) -> instaloader.Instaloader:
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        save_metadata=False,
        quiet=True,
        max_connection_attempts=2,
    )
    if session_user:
        L.load_session_from_file(session_user)
    return L


def _media(post: instaloader.Post) -> list[FetchedMedia]:
    if post.typename == "GraphSidecar":
        return [
            FetchedMedia("video" if n.is_video else "image", n.video_url if n.is_video else n.display_url, None, None)
            for n in post.get_sidecar_nodes()
        ]
    dims = post._node.get("dimensions", {})
    url = post.video_url if post.is_video else post.url
    return [FetchedMedia("video" if post.is_video else "image", url, dims.get("width"), dims.get("height"))]


def fetch_profile(L: instaloader.Instaloader, username: str, since: datetime | None, limit: int) -> FetchedProfile:
    try:
        profile = instaloader.Profile.from_username(L.context, username)
    except (instaloader.ProfileNotExistsException, instaloader.LoginRequiredException) as e:
        raise AccountUnavailable(str(e)) from e
    if profile.is_private:
        raise AccountUnavailable(f"@{username} is private")

    posts: list[FetchedPost] = []