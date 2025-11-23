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