"""RQ jobs. The worker runs these synchronously, one account at a time, spaced out: Instagram
rate-limits by IP, and a burst of forty profiles is what gets a server blocked."""

import asyncio
from datetime import UTC, datetime

from redis import Redis