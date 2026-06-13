# Automatic ONNX Model Deployment System

This repository implements an automatic deployment system for an ONNX image classification model using **FastAPI**, **ONNX Runtime**, **Docker**, **GitHub Actions** and a cloud server.

The project is designed for a course assignment where a model already exists in production and new ONNX models must be deployed automatically through CI/CD.

## General objective

Automate the deployment of an ONNX model so users can consume it through HTTP endpoints without manually installing dependencies, copying files, or starting services.

## Main characteristics

- The ONNX model is **not stored in this repository**.
- The model is downloaded from external storage using the `MODEL_URL` environment variable.
- Test data is also downloaded from external storage using `TEST_IMAGE_URL`.
- There are two branches and two deployment environments:
  - `dev` for development.
  - `prod` for production.
- Each branch has its own GitHub Actions pipeline.
- Each environment exposes a different endpoint.
- Each prediction is stored in a TXT log file.
- The log file can optionally be synchronized to an AWS S3 bucket.

## Proposed cloud architecture

```text
GitHub repository
│
├── Branch dev
│   └── GitHub Actions pipeline
│       ├── Download test data
│       ├── Download ONNX model
│       ├── Run tests
│       ├── Build Docker image
│       ├── Push Docker image to GHCR
│       └── Deploy DEV container
│
├── Branch prod
│   └── GitHub Actions pipeline
│       ├── Download test data
│       ├── Download ONNX model
│       ├── Run tests
│       ├── Build Docker image
│       ├── Push Docker image to GHCR
│       └── Deploy PROD container
│
├── External model storage
│   └── resnet50.onnx
│
├── External test data storage
│   └── car_test.jpg
│
└── Cloud server
    ├── DEV endpoint  -> http://SERVER_IP:8001
    └── PROD endpoint -> http://SERVER_IP:8002
```

## Repository structure

```text
onnx-auto-deployment/
│
├── app/
│   ├── main.py
│   ├── model.py
│   ├── preprocessing.py
│   ├── config.py
│   └── utils.py
│
├── tests/
│   ├── test_model_load.py
│   ├── test_prediction_shape.py
│   └── test_prediction_metric.py
│
├── scripts/
│   ├── download_model.py
│   ├── download_test_data.py
│   ├── smoke_test_endpoint.py
│   └── upload_prediction_log.py
│
├── .github/
│   └── workflows/
│       ├── deploy-dev.yml
│       └── deploy-prod.yml
│
├── docs/
│   ├── deployment_guide.md
│   ├── demo_script.md
│   └── grading_alignment.md
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## API endpoints

### Health check

```bash
GET /health
```

### Prediction

```bash
POST /predict
```

Example:

```bash
curl -X POST "http://SERVER_IP:8001/predict" \
  -F "file=@data/test/car_test.jpg"
```

## Local execution

1. Create a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`.

```bash
cp .env.example .env
```

4. Export environment variables.

Linux/macOS:

```bash
export MODEL_URL="https://your-bucket.s3.amazonaws.com/models/resnet50.onnx"
export TEST_IMAGE_URL="https://your-bucket.s3.amazonaws.com/test-data/car_test.jpg"
```

Windows PowerShell:

```powershell
$env:MODEL_URL="https://your-bucket.s3.amazonaws.com/models/resnet50.onnx"
$env:TEST_IMAGE_URL="https://your-bucket.s3.amazonaws.com/test-data/car_test.jpg"
```

5. Download the test data.

```bash
python scripts/download_test_data.py
```

6. Run tests.

```bash
pytest tests/ -q
```

7. Start the API.

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

8. Test the prediction endpoint.

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@data/test/car_test.jpg"
```

## Docker execution

```bash
docker build -t onnx-api .
docker run -d \
  --name onnx-api \
  -p 8000:8000 \
  -e MODEL_URL="https://your-bucket.s3.amazonaws.com/models/resnet50.onnx" \
  -e PREDICTION_LOG_PATH="predictions_local.txt" \
  onnx-api
```

## GitHub secrets required

Create the following secrets in:

```text
GitHub repository -> Settings -> Secrets and variables -> Actions
```

Required secrets:

```text
MODEL_URL
TEST_MODEL
TEST_IMAGE_URL
EC2_HOST
EC2_USER
EC2_SSH_KEY
```

`MODEL_URL` is the model deployed to the running container. `TEST_MODEL` is the model downloaded during the `test` stage (it can point to the same file or to a smaller/faster ONNX model for CI).

Optional S3 log secrets:

```text
PREDICTION_BUCKET
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
```

## Branch strategy

| Branch | Pipeline | Endpoint |
|---|---|---|
| `dev` | `.github/workflows/deploy-dev.yml` | `http://SERVER_IP:8001` |
| `prod` | `.github/workflows/deploy-prod.yml` | `http://SERVER_IP:8002` |

## Pipeline stages

Each pipeline executes the minimum required stages:

1. `test`: downloads test data and runs unit tests.
2. `build/promote`: builds and publishes the Docker image.
3. `deploy`: updates the corresponding cloud endpoint.

## Important note about the ONNX model

The `.onnx` file must not be committed to this repository. The system downloads it during execution using `MODEL_URL`. This satisfies the requirement that the model lives in an external bucket, warehouse, database, or equivalent storage.

## Prediction logs

Every call to `/predict` appends one line to a TXT file:

- DEV: `predictions_dev.txt`
- PROD: `predictions_prod.txt`

If S3 variables are configured, the file is synchronized to the selected S3 bucket.
