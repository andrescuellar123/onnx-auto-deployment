from fastapi import FastAPI, File, UploadFile

from app.model import get_session, predict_image
from app.utils import save_prediction_log

app = FastAPI(
    title="ONNX Automatic Deployment API",
    description="FastAPI service for serving an externally stored ONNX model.",
    version="1.0.0",
)


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
    log_info = save_prediction_log(prediction)

    return {
        "filename": file.filename,
        "prediction": prediction,
        "log": log_info,
    }
