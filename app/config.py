import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    app_env: str = os.getenv("APP_ENV", "local")
    model_url: str | None = os.getenv("MODEL_URL")
    model_path: str = os.getenv("MODEL_PATH", "models/resnet50.onnx")
    prediction_log_path: str = os.getenv("PREDICTION_LOG_PATH", "predictions.txt")
    prediction_bucket: str | None = os.getenv("PREDICTION_BUCKET")
    prediction_bucket_key: str | None = os.getenv("PREDICTION_BUCKET_KEY")
    expected_class_ids: str | None = os.getenv("EXPECTED_CLASS_IDS")
    min_confidence: float = float(os.getenv("MIN_CONFIDENCE", "0.80"))


settings = Settings()
