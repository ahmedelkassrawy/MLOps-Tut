# Docker Setup

This directory contains all Docker-related files for the MLOps Water Potability API.

## Files

- `Dockerfile` - Main Docker image definition
- `docker-compose.yml` - Multi-service setup (API + MLflow)
- `deploy.sh` - Deployment automation script

## Quick Start

**From project root directory:**

```bash
# Build and run API only
./docker.sh run

# Build and run API + MLflow UI
./docker.sh compose

# Stop all services
./docker.sh stop
```

## Manual Commands

**Build image:**
```bash
docker build -f src/docker/Dockerfile -t mlops-water-api .
```

**Run container:**
```bash
docker run -p 8000:8000 mlops-water-api
```

**Run with docker-compose:**
```bash
docker-compose -f src/docker/docker-compose.yml up -d
```

## Services

- **API**: http://localhost:8000 (FastAPI with model predictions)
- **MLflow UI**: http://localhost:5000 (experiment tracking)

## Requirements

- Docker installed
- Model trained (`model.pkl` exists in project root)
- Run commands from project root directory