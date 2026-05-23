from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from gramfeed.fetch import stories


def test_story_media_is_rehosted_immediately(monkeypatch):