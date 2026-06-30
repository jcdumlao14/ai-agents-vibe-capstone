# Deployment Guide

This guide shows how to deploy the BusinessPilot AI platform for local development, Docker container deployment, Google Cloud Run, Render, Railway, and GitHub Actions CI/CD.

## Local Docker Deployment

### Build

```bash
cd /workspaces/ai-agents-vibe-capstone
docker build -t businesspilot-ai:latest .
```

### Run

```bash
docker run --rm -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e PROJECT_ID=$PROJECT_ID \
  -e GOOGLE_REGION=$GOOGLE_REGION \
  -e GOOGLE_ADK_ENDPOINT_ID=$GOOGLE_ADK_ENDPOINT_ID \
  -e USE_GOOGLE_ADK=$USE_GOOGLE_ADK \
  -e GOOGLE_ANTIGRAVITY_ENDPOINT=$GOOGLE_ANTIGRAVITY_ENDPOINT \
  -e GOOGLE_ANTIGRAVITY_API_KEY=$GOOGLE_ANTIGRAVITY_API_KEY \
  -e USE_GOOGLE_ANTIGRAVITY=$USE_GOOGLE_ANTIGRAVITY \
  businesspilot-ai:latest
```

### Docker Compose

The repository includes a sample `docker-compose.yml` for local development.

```bash
docker compose up --build
```

> The app listens on port `8000` and exposes the FastAPI service at `http://localhost:8000`.

## Local Uvicorn Run

```bash
uvicorn src.services.api:app --host 0.0.0.0 --port 8000
```

## Google Cloud Run

This project is designed to run as a containerized FastAPI service on Cloud Run.

### Prerequisites

- `gcloud` CLI installed and authenticated
- Google Cloud project configured
- Cloud Run API enabled
- Service account with `roles/run.admin`, `roles/storage.admin`, and `roles/iam.serviceAccountUser`

### Build and push image

```bash
cd /workspaces/ai-agents-vibe-capstone
PROJECT_ID=your-gcp-project-id
IMAGE_NAME=gcr.io/$PROJECT_ID/businesspilot-ai:latest

gcloud builds submit --tag "$IMAGE_NAME" .
```

### Deploy to Cloud Run

```bash
gcloud run deploy businesspilot-ai \
  --image "$IMAGE_NAME" \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "OPENAI_API_KEY=$OPENAI_API_KEY,PROJECT_ID=$PROJECT_ID,GOOGLE_REGION=$GOOGLE_REGION,GOOGLE_ADK_ENDPOINT_ID=$GOOGLE_ADK_ENDPOINT_ID,USE_GOOGLE_ADK=$USE_GOOGLE_ADK,GOOGLE_ANTIGRAVITY_ENDPOINT=$GOOGLE_ANTIGRAVITY_ENDPOINT,GOOGLE_ANTIGRAVITY_API_KEY=$GOOGLE_ANTIGRAVITY_API_KEY,USE_GOOGLE_ANTIGRAVITY=$USE_GOOGLE_ANTIGRAVITY"
```

### Cloud Run Environment Variables

Set these environment variables for production deployments:

- `OPENAI_API_KEY`
- `PROJECT_ID`
- `GOOGLE_REGION`
- `GOOGLE_ADK_ENDPOINT_ID`
- `USE_GOOGLE_ADK`
- `GOOGLE_ANTIGRAVITY_ENDPOINT`
- `GOOGLE_ANTIGRAVITY_API_KEY`
- `USE_GOOGLE_ANTIGRAVITY`
- `DATASET_NAME`
- `MODEL_NAME`

## Render Deployment

Render can deploy the repository directly from GitHub using the existing `Dockerfile`.

### Render setup

1. Create a new Web Service in Render.
2. Connect your GitHub repository.
3. Choose `Docker` as the environment.
4. Set the start command to:

```bash
uvicorn src.services.api:app --host 0.0.0.0 --port 8000
```

5. Add these environment variables in Render:

- `OPENAI_API_KEY`
- `PROJECT_ID`
- `GOOGLE_REGION`
- `GOOGLE_ADK_ENDPOINT_ID`
- `USE_GOOGLE_ADK`
- `GOOGLE_ANTIGRAVITY_ENDPOINT`
- `GOOGLE_ANTIGRAVITY_API_KEY`
- `USE_GOOGLE_ANTIGRAVITY`

6. Deploy and verify `/health` returns `{"status":"ok"}`.

## Railway Deployment

Railway supports Docker-based deployment and can run this service with the existing repository.

### Railway setup

1. Create a new Railway project.
2. Import the GitHub repository.
3. Select `Docker` as the deployment mode.
4. Use this start command:

```bash
uvicorn src.services.api:app --host 0.0.0.0 --port 8000
```

5. Add the same environment variables as above.
6. Deploy and confirm the service is reachable.

## GitHub Actions CI/CD

This repository includes a GitHub Actions workflow at `.github/workflows/ci-cd.yml` that runs:

- Python dependency install
- Syntax validation with `python -m py_compile`
- `pytest` execution
- Google Cloud Run deployment on `main`

### Required repository secrets

- `GCP_PROJECT_ID`
- `GCP_SA_KEY`
- `CLOUD_RUN_SERVICE`
- `CLOUD_RUN_REGION`
- `OPENAI_API_KEY`
- `GOOGLE_REGION`
- `GOOGLE_ADK_ENDPOINT_ID`
- `USE_GOOGLE_ADK`
- `GOOGLE_ANTIGRAVITY_ENDPOINT`
- `GOOGLE_ANTIGRAVITY_API_KEY`
- `USE_GOOGLE_ANTIGRAVITY`

### Notes

- Keep secrets and API keys secure.
- Use the `.env.example` file as a template for local development.
- Confirm the service health after deployment with `/health`.
- For Cloud Run, inspect deployment details with:

```bash
gcloud run services describe businesspilot-ai --region us-central1
```
