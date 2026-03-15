"""The clock process: queues every account once per refresh interval."""

import time

from gramfeed.fetch.jobs import schedule_all