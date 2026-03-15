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
    key = f"{prefix}/{hashlib.sha1(path.encode()).hexdigest()[:16]}{ext}"
    try:
        _s3.head_object(Bucket=settings().s3_bucket, Key=key)
        return key
    except _s3.exceptions.ClientError:
        pass
    with httpx.stream("GET", url, timeout=60, follow_redirects=True) as r:
        r.raise_for_status()
        _s3.upload_fileobj(
            r.iter_raw(),  # type: ignore[arg-type]
            settings().s3_bucket,
            key,
            ExtraArgs={"ContentType": r.headers.get("content-type", "image/jpeg"), "CacheControl": "public, max-age=31536000"},
        )
    return key

