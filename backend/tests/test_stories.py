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