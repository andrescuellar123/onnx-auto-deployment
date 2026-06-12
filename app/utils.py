from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.config import settings


def append_prediction_log(result: dict) -> str:
    """Append one prediction line to a TXT file and return the line written."""
    timestamp = datetime.now(timezone.utc).isoformat()
    log_line = f"{timestamp} | {json.dumps(result, ensure_ascii=False)}\n"

    log_path = Path(settings.prediction_log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a", encoding="utf-8") as file:
        file.write(log_line)

    return log_line


def upload_prediction_log_to_s3() -> bool:
    """Upload the local prediction log to S3 when S3 settings are available.

    This keeps the project usable without AWS credentials during local demos, while
    still satisfying the cloud-storage design required for the final deployment.
    """
    if not settings.prediction_bucket:
        return False

    local_path = Path(settings.prediction_log_path)
    if not local_path.exists():
        return False

    key = settings.prediction_bucket_key or local_path.name

    try:
        s3 = boto3.client("s3")
        s3.upload_file(str(local_path), settings.prediction_bucket, key)
        return True
    except (BotoCoreError, ClientError) as exc:
        print(f"Warning: prediction log could not be uploaded to S3: {exc}")
        return False


def save_prediction_log(result: dict) -> dict:
    """Save the prediction locally and optionally synchronize it with S3."""
    append_prediction_log(result)
    uploaded = upload_prediction_log_to_s3()

    return {
        "local_log": settings.prediction_log_path,
        "s3_uploaded": uploaded,
        "s3_bucket": settings.prediction_bucket,
        "s3_key": settings.prediction_bucket_key,
    }
