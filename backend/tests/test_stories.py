from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from gramfeed.fetch import stories


def test_story_media_is_rehosted_immediately(monkeypatch):
    calls = []
    monkeypatch.setattr(stories, "rehost", lambda url, prefix: calls.append((url, prefix)) or "alice/stories/1.jpg")
    item = SimpleNamespace(
        mediaid=1,
        is_video=False,
        url="https://cdn.instagram.test/story.jpg",
        date_utc=datetime(2026, 5, 1, 12, tzinfo=UTC),
        expiring_utc=datetime(2026, 5, 2, 12, tzinfo=UTC),
        caption="rainbow",
        _node={"dimensions": {"width": 1080, "height": 1920}},
    )
    media = stories._story_media(item, "alice")
    assert media.kind == "image"
    assert media.key == "alice/stories/1.jpg"