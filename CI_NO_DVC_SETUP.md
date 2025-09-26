# GitHub Actions CI/CD Setup - No DVC Dependencies

## Overview ✅

This setup removes DVC dependencies from GitHub Actions while maintaining Docker build capabilities. The CI pipeline now uses a simplified approach with a dummy model for containerization.

## What Changed

### ❌ **Removed from CI:**
- DVC pipeline execution (`dvc repro`)
- Complex model training in CI
- DVC validation steps
- MLflow dependencies in CI

### ✅ **Added to CI:**
- Lightweight dummy model generation
- Simple validation script (`validate-ci.sh`)
- CI-specific Dockerfile (`Dockerfile.ci`)
- Scikit-learn based placeholder model

## File Structure

```
├── .github/workflows/docker-build.yml    # Updated CI workflow
├── src/docker/
│   ├── Dockerfile                        # Production Docker (uses real model)
│   └── Dockerfile.ci                     # CI Docker (uses dummy model)
├── scripts/
│   ├── validate-pipeline.sh              # Local DVC validation (for dev)
│   └── validate-ci.sh                   # CI validation (no DVC)
└── model.pkl                           # Real model (local) or dummy (CI)
```

## GitHub Actions Workflow

### **Steps:**
1. **Checkout code**
2. **Setup Python 3.12**
3. **Install basic dependencies** (fastapi, uvicorn, scikit-learn, pandas)
4. **Create dummy model** using scikit-learn RandomForestClassifier
5. **Validate environment** using `scripts/validate-ci.sh`
6. **Login to Docker Hub**
7. **Build and push Docker image** using `Dockerfile.ci`

### **Generated Docker Tags:**
- `{username}/mlops-water-api:ci-latest` (latest CI build)
- `{username}/mlops-water-api:ci-{sha}` (specific commit)

## Local vs CI Differences

### **Local Development:**
```bash
# Use real DVC pipeline
dvc repro

# Build production Docker
docker build -f src/docker/Dockerfile -t mlops-water-api .

# Real trained RandomForest model
```

### **CI Environment:**
```bash
# Use dummy model generator
python3 create_dummy_model.py

# Build CI Docker  
docker build -f src/docker/Dockerfile.ci -t mlops-water-api:ci .

# Dummy RandomForest with random training data
```

## API Response Differences

### **Production API:**
```json
{
  "message": "Water Potability Prediction API",
  "version": "1.0.0", 
  "model_type": "production",
  "status": "running"
}
```

### **CI API:**
```json
{
  "message": "Water Potability Prediction API",
  "version": "1.0.0",
  "model_type": "ci_dummy_classifier", 
  "status": "running"
}
```

## Benefits

### ✅ **Advantages:**
- **Faster CI builds**: No DVC pipeline execution
- **Reduced complexity**: Fewer dependencies in CI
- **More reliable**: No DVC validation failures
- **Parallel development**: CI doesn't block on ML pipeline issues
- **Resource efficient**: Less compute time in GitHub Actions

### ⚠️ **Trade-offs:**
- **CI model isn't real**: Uses dummy predictions
- **Two Dockerfiles**: Need to maintain both production and CI versions
- **Manual model deployment**: Real models need separate deployment process

## Usage

### **For CI/CD:**
```bash
# GitHub Actions automatically:
# 1. Creates dummy model
# 2. Builds CI Docker image  
# 3. Pushes to registry with 'ci-' prefix
```

### **For Production:**
```bash
# Local development:
dvc repro                                    # Generate real model
docker build -f src/docker/Dockerfile .     # Build with real model
docker push your-registry/mlops-water-api   # Deploy production
```

### **For Development:**
```bash
# Test CI validation locally:
./scripts/validate-ci.sh

# Test production validation locally:  
./scripts/validate-pipeline.sh
```

## Required GitHub Secrets

Same as before:
- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token

## Deployment Strategy

1. **CI builds** → Use for testing/staging with dummy predictions
2. **Production builds** → Manual process with real DVC-generated models
3. **Model updates** → Run DVC pipeline locally, build production Docker separately

## Next Steps

Consider implementing:
- Separate production deployment workflow
- Model artifact storage (S3, MLflow Model Registry)
- Automated model validation tests
- Blue/green deployment for model updates