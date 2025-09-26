# MLOps Tutorial - Water Potability Prediction

This project demonstrates MLOps practices using DVC (Data Version Control) and MLflow for tracking machine learning experiments. The project predicts water potability using a RandomForest classifier.

## Project Structure

```
├── data/
│   ├── water_potability.csv      # Original dataset
│   ├── raw/                      # Raw data splits
│   └── processed/                # Preprocessed data
├── src/
│   ├── data_collection.py        # Data splitting
│   ├── data_prep.py             # Data preprocessing
│   ├── model_building.py        # Model training
│   ├── model_eval.py            # Model evaluation
│   └── api/                     # FastAPI service
├── dvc.yaml                     # DVC pipeline definition
├── params.yaml                  # Model parameters
├── requirements.txt             # Python dependencies
├── model.pkl                    # Trained model
└── mlruns/                      # MLflow tracking data
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize DVC (if not already done):**
   ```bash
   dvc init
   ```

## Running with DVC

DVC manages our machine learning pipeline with the following stages:

### 1. Run the Complete Pipeline

Execute all stages in the correct order:
```bash
dvc repro
```

This will run:
- Data collection (splitting)
- Data preprocessing
- Model training
- Model evaluation

### 2. Run Individual Stages

You can run specific stages:

```bash
# Data collection only
dvc repro data_collection

# Data preprocessing only
dvc repro data_preprocessing

# Model training only
dvc repro model_training

# Model evaluation only
dvc repro model_evaluation
```

### 3. View Pipeline Status

Check which stages need to be re-run:
```bash
dvc status
```

### 4. Visualize Pipeline

Generate a visual representation of the pipeline:
```bash
dvc dag
```

### 5. Show Metrics

View current metrics:
```bash
dvc metrics show
```

Compare metrics across experiments:
```bash
dvc metrics diff
```

### 6. Show Plots

Display performance plots:
```bash
dvc plots show
```

### 7. Parameter Management

Edit parameters in `params.yaml`:
```yaml
data_collection:
  test_size: 0.20

model_building:
  n_estimators: 100
```

After changing parameters, run:
```bash
dvc repro
```

## Running with MLflow

MLflow tracks experiments, parameters, metrics, and artifacts.

### 1. Start MLflow UI

Launch the MLflow tracking server:
```bash
mlflow ui
```

By default, this starts a server at `http://localhost:5000`

### 2. View Experiments

Open your browser and navigate to `http://localhost:5000` to:
- Compare different experiment runs
- View metrics (accuracy, precision, recall, f1-score)
- Download trained models
- Visualize performance plots

### 3. Run Experiments with MLflow Tracking

The model training script (`src/model_building.py`) automatically logs:
- Parameters (n_estimators, etc.)
- Metrics (accuracy, precision, recall, f1-score)
- Model artifacts
- Training plots

Each run creates a new experiment entry in MLflow.

### 4. MLflow CLI Commands

```bash
# List experiments
mlflow experiments list

# Search runs
mlflow runs list --experiment-id 0

# Serve a model
mlflow models serve -m runs:/<run-id>/model -p 1234
```

## FastAPI Service

Run the prediction API:

```bash
# Start the API server
cd src/api
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Workflow Examples

### Complete Experiment Run

1. **Modify parameters** in `params.yaml`
2. **Run pipeline:** `dvc repro`
3. **View results:** `mlflow ui`
4. **Compare experiments** in MLflow UI

### Reproduce Specific Experiment

1. **Check pipeline status:** `dvc status`
2. **Run specific stage:** `dvc repro model_training`
3. **View metrics:** `dvc metrics show`

### Data Versioning

```bash
# Add data to DVC tracking
dvc add data/water_potability.csv

# Commit changes
git add data/water_potability.csv.dvc .gitignore
git commit -m "Add water potability dataset"

# Push data to remote storage (if configured)
dvc push
```

## Key Features

- **Reproducible Pipelines**: DVC ensures consistent execution
- **Experiment Tracking**: MLflow logs all experiments automatically  
- **Parameter Management**: Centralized configuration in `params.yaml`
- **Model Versioning**: Both DVC and MLflow track model versions
- **API Deployment**: FastAPI service for model predictions

## Troubleshooting

1. **Pipeline Issues**: Check `dvc status` for dependency problems
2. **MLflow UI**: Ensure port 5000 is available
3. **Missing Dependencies**: Run `pip install -r requirements.txt`
4. **Data Issues**: Verify data files exist in expected locations

## Next Steps

- Configure remote storage for DVC (S3, GCS, etc.)
- Set up MLflow remote tracking server
- Add more sophisticated model evaluation metrics
- Implement CI/CD pipeline integration