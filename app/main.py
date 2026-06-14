from fastapi import FastAPI, File, UploadFile

from app.model import get_session, predict_image
from app.utils import download_prediction_log_from_s3, save_prediction_log

app = FastAPI(
    title="ONNX Automatic Deployment API",
    description="FastAPI service for serving an externally stored ONNX model.",
    version="1.0.0",
)


@app.on_event("startup")
def restore_prediction_log() -> None:
    download_prediction_log_from_s3()


@app.get("/")
def root() -> dict:
    return {
        "message": "ONNX Automatic Deployment API is running",
        "docs": "/docs",
        "health": "/health",
        "prediction_endpoint": "/predict",
    }


@app.get("/health")
def health() -> dict:
    session = get_session()
    return {
        "status": "ok",
        "model_loaded": True,
        "inputs": [item.name for item in session.get_inputs()],
        "outputs": [item.name for item in session.get_outputs()],
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> dict:
    image_bytes = await file.read()
    prediction = predict_image(image_bytes)
    save_prediction_log(prediction)

    return {
        "filename": file.filename,
        "prediction": {
            "predicted_class_name": prediction["predicted_class_name"],
            "confidence": prediction["confidence"],
        },
    }
