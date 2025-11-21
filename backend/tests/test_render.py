from datetime import UTC, datetime
from types import SimpleNamespace

from gramfeed.feeds.render import item_html, title_of


def post(caption=None, kind="image", media=(), location=None):
    return SimpleNamespace(caption=caption, kind=kind, media=list(media), location=location,
                           shortcode="C1", taken_at=datetime(2026, 5, 1, tzinfo=UTC))


def test_title_is_first_caption_line_cut_at_a_word():
    long = "Morning light over the harbour, with the fishing boats coming back after a long night at sea"
    assert title_of(post(long + "\nsecond line")).endswith("…")
    assert len(title_of(post(long))) <= 81
    assert title_of(post("Short one\nmore")) == "Short one"


def test_title_falls_back_to_the_kind_of_post():