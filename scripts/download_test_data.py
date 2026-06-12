import os
import urllib.request
from pathlib import Path

TEST_IMAGE_URL = os.getenv("TEST_IMAGE_URL")
TEST_IMAGE_PATH = Path(os.getenv("TEST_IMAGE_PATH", "data/test/car_test.jpg"))


def main() -> None:
    if not TEST_IMAGE_URL:
        raise RuntimeError("TEST_IMAGE_URL environment variable is required.")

    TEST_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading test image from {TEST_IMAGE_URL}")
    urllib.request.urlretrieve(TEST_IMAGE_URL, TEST_IMAGE_PATH)
    print(f"Test image available at: {TEST_IMAGE_PATH}")


if __name__ == "__main__":
    main()
