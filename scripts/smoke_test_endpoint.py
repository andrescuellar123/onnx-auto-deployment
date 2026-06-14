import os
from pathlib import Path

import requests

ENDPOINT_URL = os.getenv("ENDPOINT_URL", "http://localhost:8000/predict")
TEST_IMAGE_PATH = Path(os.getenv("TEST_IMAGE_PATH", "data/test/test_img.jpg"))


def main() -> None:
    if not TEST_IMAGE_PATH.exists():
        raise RuntimeError(f"Test image not found: {TEST_IMAGE_PATH}")

    with TEST_IMAGE_PATH.open("rb") as file:
        response = requests.post(ENDPOINT_URL, files={"file": file}, timeout=30)

    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    main()
