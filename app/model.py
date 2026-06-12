import os
import urllib.request
from pathlib import Path

import numpy as np
import onnxruntime as ort

from app.config import settings
from app.preprocessing import preprocess_image

_session: ort.InferenceSession | None = None


def download_model() -> Path:
    """Download the ONNX model from external storage if it is not available locally."""
    model_path = Path(settings.model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    if model_path.exists() and model_path.stat().st_size > 0:
        return model_path

    if not settings.model_url:
        raise RuntimeError(
            "MODEL_URL is not defined. The ONNX model must be downloaded from "
            "external storage, not stored in the repository."
        )

    print(f"Downloading ONNX model from {settings.model_url}")
    urllib.request.urlretrieve(settings.model_url, model_path)

    if not model_path.exists() or model_path.stat().st_size == 0:
        raise RuntimeError("The ONNX model could not be downloaded correctly.")

    return model_path


def get_session() -> ort.InferenceSession:
    """Return a cached ONNX Runtime inference session."""
    global _session

    if _session is None:
        model_path = download_model()
        providers = ["CPUExecutionProvider"]
        _session = ort.InferenceSession(str(model_path), providers=providers)

    return _session


def softmax(values: np.ndarray) -> np.ndarray:
    """Compute softmax safely for model logits."""
    values = values.astype(np.float64)
    exp_values = np.exp(values - np.max(values))
    return exp_values / np.sum(exp_values)


def predict_image(image_bytes: bytes) -> dict:
    """Run image classification over an uploaded image."""
    session = get_session()

    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    image_array = preprocess_image(image_bytes)
    outputs = session.run([output_name], {input_name: image_array})

    scores = outputs[0][0]
    probabilities = softmax(scores)
    predicted_class = int(np.argmax(probabilities))
    confidence = float(np.max(probabilities))

    return {
        "environment": os.getenv("APP_ENV", settings.app_env),
        "predicted_class": predicted_class,
        "confidence": round(confidence, 6),
        "input_name": input_name,
        "output_name": output_name,
    }
