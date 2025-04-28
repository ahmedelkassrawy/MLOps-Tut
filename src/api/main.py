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

@app.get("/")  # Add the '@' decorator
async def main():
    return {"message": "Hello World"}

with open("/workspaces/MLOps-Tut/model.pkl", "rb") as f:
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

