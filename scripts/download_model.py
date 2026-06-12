"""Download the ONNX model from the MODEL_URL environment variable."""

from app.model import download_model


if __name__ == "__main__":
    path = download_model()
    print(f"Model available at: {path}")
