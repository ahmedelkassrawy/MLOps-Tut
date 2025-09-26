import pandas as pd
import os
import numpy as np

train_data = pd.read_csv("/workspaces/MLOps-Tut/data/raw/train_csv")
test_data = pd.read_csv("/workspaces/MLOps-Tut/data/raw/test_csv")

def fill_missing(df):
    for column in df.columns:
        if df[column].isnull().sum() > 0:
            median_value = df[column].median()
            df[column].fillna(median_value, inplace=True)
    return df

train_processed_data = fill_missing(train_data)
test_processed_data = fill_missing(test_data)

data_path = os.path.join("data", "processed")
os.makedirs(data_path, exist_ok=True)  

train_processed_data.to_csv(os.path.join(data_path, "train_processed.csv"), index=False)
test_processed_data.to_csv(os.path.join(data_path, "test_processed.csv"), index=False)

