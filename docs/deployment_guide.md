# Deployment guide

## 1. Create the GitHub repository

Create a new repository and upload all files from this project.

Then create two branches:

```bash
git checkout -b dev
git push origin dev

git checkout -b prod
git push origin prod
```

## 2. Upload external assets

Upload these files to external storage, for example AWS S3:

```text
models/resnet50.onnx
test-data/test_img.jpg
```

The ONNX model must not be stored in GitHub.

## 3. Configure GitHub secrets

Required:

```text
MODEL_URL
TEST_MODEL
TEST_IMAGE_URL
EC2_HOST
EC2_USER
EC2_SSH_KEY
```

`TEST_MODEL` is the ONNX model downloaded for the `test` stage (can be the same as `MODEL_URL` or a smaller one for faster CI runs).

Optional for S3 prediction logs:

```text
PREDICTION_BUCKET
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
```

## 4. Prepare the EC2 server

Install Docker on the server:

```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

Open the following ports in the EC2 security group:

```text
22    SSH
8001  DEV API
8002  PROD API
```

## 5. Deploy DEV

Push to the `dev` branch:

```bash
git checkout dev
git add .
git commit -m "Initial DEV deployment"
git push origin dev
```

The DEV pipeline will deploy the API on:

```text
http://SERVER_IP:8001
```

## 6. Deploy PROD

Merge or push to the `prod` branch:

```bash
git checkout prod
git merge dev
git push origin prod
```

The PROD pipeline will deploy the API on:

```text
http://SERVER_IP:8002
```

## 7. Validate the deployment

DEV:

```bash
curl http://SERVER_IP:8001/health
```

PROD:

```bash
curl http://SERVER_IP:8002/health
```

Prediction example:

```bash
curl -X POST "http://SERVER_IP:8001/predict" \
  -F "file=@test_img.jpg"
```
