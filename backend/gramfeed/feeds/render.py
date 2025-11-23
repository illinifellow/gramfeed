"""RSS 2.0 and Atom from stored posts. Each item carries its images inline, so a reader shows the
post as Instagram would, and the first image as an enclosure for readers that only show those."""

from html import escape

from feedgen.feed import FeedGenerator

from gramfeed.db.models import Account
from gramfeed.fetch.media import public_url
from gramfeed.settings import settings


def item_html(account: Account, post) -> str:
    parts = []
    for m in post.media:
        url = public_url(m.key)
        if m.kind == "video":
            parts.append(f'<video src="{url}" controls playsinline></video>')
        else:
            parts.append(f'<img src="{url}" alt="" loading="lazy">')
    if post.caption:
        parts.append("<p>" + escape(post.caption).replace("\n", "<br>") + "</p>")
    if post.location:
        parts.append(f"<p><small>📍 {escape(post.location)}</small></p>")
    return "\n".join(parts)


def title_of(post) -> str:
    """The first line of the caption, cut at a word, or the kind of post."""
    first = (post.caption or "").strip().split("\n", 1)[0]
    if not first:
        return {"video": "Video", "carousel": "Photos"}.get(post.kind, "Photo")
    return first if len(first) <= 80 else first[:80].rsplit(" ", 1)[0] + "…"


def build(account: Account, fmt: str) -> bytes:
    fg = FeedGenerator()
    fg.id(f"{settings().public_url}/{account.username}")
    fg.title(f"{account.full_name or account.username} (@{account.username})")
    fg.link(href=f"https://www.instagram.com/{account.username}/", rel="alternate")
    fg.link(href=f"{settings().public_url}/{account.username}.{fmt}", rel="self")
    fg.description(account.biography or f"Posts from @{account.username}")
    if account.avatar_key:
        fg.logo(public_url(account.avatar_key))
    for post in reversed(account.posts[: settings().max_posts_per_feed]):
        e = fg.add_entry()
        e.id(f"https://www.instagram.com/p/{post.shortcode}/")
        e.link(href=f"https://www.instagram.com/p/{post.shortcode}/")