import hashlib
import mimetypes

import boto3
import httpx

from gramfeed.settings import settings

_s3 = boto3.client("s3", endpoint_url=settings().s3_endpoint)


def rehost(url: str, prefix: str) -> str:
    """Copies an Instagram CDN file to our bucket; the key is stable, so a re-fetch is free."""
    path = url.split("?")[0]
    ext = mimetypes.guess_extension(mimetypes.guess_type(path)[0] or "image/jpeg") or ".jpg"