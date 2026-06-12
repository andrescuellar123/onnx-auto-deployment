"""Upload the configured prediction log file to S3."""

from app.utils import upload_prediction_log_to_s3


if __name__ == "__main__":
    uploaded = upload_prediction_log_to_s3()
    print(f"Uploaded to S3: {uploaded}")
