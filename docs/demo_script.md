# Demo script for final presentation

## 1. Introduction

This project implements an automatic deployment system for an ONNX image classification model. The objective is to allow new models to be deployed automatically through a CI/CD pipeline whenever changes are pushed to the `dev` or `prod` branches.

## 2. Repository structure

Show the repository folders:

- `app`: FastAPI application and ONNX inference code.
- `tests`: unit tests for the model.
- `scripts`: support scripts for downloading external data and testing endpoints.
- `.github/workflows`: GitHub Actions pipelines.
- `docs`: deployment guide and project documentation.

Explain that the `.onnx` model is not stored in GitHub. It is downloaded from external storage using `MODEL_URL`.

## 3. CI/CD pipeline

Open `.github/workflows/deploy-dev.yml` and explain the stages:

1. Checkout repository.
2. Install dependencies.
3. Download test data from external storage.
4. Run unit tests.
5. Build Docker image.
6. Push Docker image.
7. Deploy the container in the DEV endpoint.

Then show `.github/workflows/deploy-prod.yml` and explain that it performs the same process for the production endpoint.

## 4. Tests

Explain the three tests:

- The first test validates that the ONNX model loads correctly.
- The second test validates that the model returns predictions with the expected output shape.
- The third test validates that the prediction confidence meets the configured threshold and optionally checks an expected class.

## 5. Endpoints

Show the two endpoints:

```text
DEV  -> http://SERVER_IP:8001
PROD -> http://SERVER_IP:8002
```

Then execute:

```bash
curl http://SERVER_IP:8001/health
```

And a prediction:

```bash
curl -X POST "http://SERVER_IP:8001/predict" \
  -F "file=@car_test.jpg"
```

## 6. Prediction logs

Explain that every request appends a new line to a TXT file:

- `predictions_dev.txt` for DEV.
- `predictions_prod.txt` for PROD.

If S3 is configured, the same file is uploaded to the bucket for later monitoring or analysis.

## 7. Closing

The solution is viable because it uses standard and lightweight tools: GitHub Actions, Docker, FastAPI, ONNX Runtime and a cloud server. It satisfies the required test, build/promote and deployment stages, while keeping the model and test data outside the repository.
