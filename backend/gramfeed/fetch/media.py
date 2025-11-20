import hashlib
import mimetypes

import boto3
import httpx

from gramfeed.settings import settings

_s3 = boto3.client("s3", endpoint_url=settings().s3_endpoint)


def rehost(url: str, prefix: str) -> str: