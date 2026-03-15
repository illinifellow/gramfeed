"""The clock process: queues every account once per refresh interval."""

import time

from gramfeed.fetch.jobs import schedule_all
from gramfeed.settings import settings

if __name__ == "__main__":
    while True:
        schedule_all()
        time.sleep(settings().refresh_minutes * 60)
