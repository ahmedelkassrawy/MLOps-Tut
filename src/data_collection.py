import pandas as pd
import numpy as np
import os
import yaml
from sklearn.model_selection import train_test_split

data = pd.read_csv("/workspaces/MLOps-Tut/data/water_potability.csv")

test_size = yaml.safe_load(open("/workspaces/MLOps-Tut/params.yaml"))["data_collection"]["test_size"]

train_data, test_data = train_test_split(data, test_size = test_size, random_state=42)

data_path = os.path.join("data", "raw")
os.makedirs(data_path, exist_ok=True)  # Allow directory creation if it already exists

train_data.to_csv(os.path.join(data_path, "train_csv"), index=False)
test_data.to_csv(os.path.join(data_path, "test_csv"), index=False)