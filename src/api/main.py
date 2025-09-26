from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
import os
import json
import numpy as np
import pickle
import uvicorn
from pydantic import BaseModel
from dvclive import Live

class Water(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

app = FastAPI()

@app.get("/")
async def main():
    model_type = getattr(model, 'model_type', 'production')
    return {
        "message": "Water Potability Prediction API", 
        "version": "1.0.0",
        "model_type": model_type,
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "API is running"}

# Load model with proper path handling
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model.pkl")
if not os.path.exists(model_path):
    # Fallback for Docker container
    model_path = "/app/model.pkl"

with open(model_path, "rb") as f:
    model = pickle.load(f)

@app.post("/predict")
async def predict(water: Water):
    sample = pd.DataFrame(
        {
            "ph": [water.ph],
            "Hardness": [water.Hardness],
            "Solids": [water.Solids],
            "Chloramines": [water.Chloramines],
            "Sulfate": [water.Sulfate],
            "Conductivity": [water.Conductivity],
            "Organic_carbon": [water.Organic_carbon],
            "Trihalomethanes": [water.Trihalomethanes],
            "Turbidity": [water.Turbidity]
        }
    )

    prediction = model.predict(sample)

    if prediction == 1:
        result = "Water is safe to drink"
    else:
        result = "Water is not safe to drink"

    return JSONResponse(content={"prediction": result})

