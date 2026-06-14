import os
from pathlib import Path

from app.config import settings
from app.model import predict_image


def test_prediction_metric_with_external_test_image():
    test_image_path = Path(os.getenv("TEST_IMAGE_PATH", "data/test/test_img.jpg"))

    assert test_image_path.exists(), (
        "The test image must be downloaded from external storage before running tests. "
        "Run scripts/download_test_data.py in the pipeline."
    )

    with test_image_path.open("rb") as file:
        result = predict_image(file.read())

    assert "predicted_class" in result
    assert "confidence" in result
    assert result["confidence"] >= settings.min_confidence

    assert "predicted_class_name" in result
    assert isinstance(result["predicted_class_name"], str)
    assert result["predicted_class_name"]

    if settings.expected_class_ids:
        expected_ids = {
            int(value.strip())
            for value in settings.expected_class_ids.split(",")
            if value.strip()
        }
        assert result["predicted_class"] in expected_ids
