import os
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import boto3

TEST_IMAGE_URL = os.getenv("TEST_IMAGE_URL")
TEST_IMAGE_PATH = Path(os.getenv("TEST_IMAGE_PATH", "data/test/test_img.jpg"))


def download_from_url(url: str, destination: Path) -> None:
    """Download a file from an http(s) URL or an s3://bucket/key URI."""
    parsed = urlparse(url)

    if parsed.scheme == "s3":
        # Fall back to us-east-1 if AWS_DEFAULT_REGION/AWS_REGION are unset or empty;
        # boto3 auto-redirects to the bucket's real region on s3.* requests.
        region = os.getenv("AWS_DEFAULT_REGION") or os.getenv("AWS_REGION") or "us-east-1"
        boto3.client("s3", region_name=region).download_file(
            parsed.netloc, parsed.path.lstrip("/"), str(destination)
        )
    else:
        urllib.request.urlretrieve(url, destination)


def main() -> None:
    if not TEST_IMAGE_URL:
        raise RuntimeError("TEST_IMAGE_URL environment variable is required.")

    TEST_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading test image from {TEST_IMAGE_URL}")
    download_from_url(TEST_IMAGE_URL, TEST_IMAGE_PATH)
    print(f"Test image available at: {TEST_IMAGE_PATH}")


if __name__ == "__main__":
    main()
