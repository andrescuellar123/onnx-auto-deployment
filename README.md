# ONNX Automatic Deployment API

FastAPI service that classifies images with a ResNet-50 ONNX model. The model
is not stored in the repository: it is downloaded from external storage
(HTTP(S) or S3) the first time the app starts. GitHub Actions automatically
deploys the `dev` and `main` branches to a `dev` and a `prod` endpoint.

## Project structure

```text
app/      - FastAPI application and ONNX inference
tests/    - unit tests
scripts/  - helper scripts (download model/test data, smoke test, upload logs)
.github/  - CI/CD pipelines (deploy-dev.yml, deploy-prod.yml)
docs/     - deployment guide and demo script
```

## Run locally

Requirements: Python 3.11+

1. Create and activate a virtual environment

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Provide the ONNX model

   Place your model file at `models/resnet50.onnx`, **or** set `MODEL_URL` to
   an `http(s)://` or `s3://bucket/key` location and it will be downloaded
   automatically on startup:

   ```bash
   export MODEL_URL="https://your-host/resnet50.onnx"   # Windows: $env:MODEL_URL="..."
   ```

4. Start the API

   ```bash
   uvicorn app.main:app --reload
   ```

5. Try it

   ```bash
   curl http://localhost:8000/health

   curl -X POST http://localhost:8000/predict \
     -F "file=@path/to/your/image.jpg"
   ```

`/predict` returns the predicted class name and confidence score. The full
result (including the numeric class id) is appended to a local log file
(`predictions.txt` by default).

## Run with Docker

```bash
docker build -t onnx-api .
docker run -d --name onnx-api -p 8000:8000 \
  -e MODEL_URL="https://your-host/resnet50.onnx" \
  onnx-api
```

## Run the tests

```bash
export TEST_IMAGE_URL="https://your-host/test_img.jpg"
python scripts/download_test_data.py
pytest tests/
```

## Configuration

Settings are read from environment variables. See [.env.example](.env.example)
for the full list and defaults. The most relevant ones for running the API:

| Variable | Purpose |
|---|---|
| `MODEL_URL` | Where to download the ONNX model from (not needed if it's already at `MODEL_PATH`) |
| `MODEL_PATH` | Local path for the model (default: `models/resnet50.onnx`) |
| `PREDICTION_LOG_PATH` | Local prediction log file (default: `predictions.txt`) |
| `PREDICTION_BUCKET` | Optional S3 bucket to sync the prediction log to |

## Deployment (dev/prod)

Pushing to the `dev` or `main` branch triggers GitHub Actions, which runs the
tests, copies the project to an EC2 instance and (re)builds/restarts the API
container there.

| Branch | Workflow | Endpoint |
|---|---|---|
| `dev` | `.github/workflows/deploy-dev.yml` | `http://SERVER_IP:8001` |
| `main` | `.github/workflows/deploy-prod.yml` | `http://SERVER_IP:8002` |

See [docs/deployment_guide.md](docs/deployment_guide.md) for the full setup
(GitHub secrets, EC2 preparation, branch strategy).
