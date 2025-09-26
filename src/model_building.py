from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import pickle
import yaml
from sklearn.metrics import accuracy_score, classification_report
import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("file:/workspaces/MLOps-Tut/mlruns")
mlflow.sklearn.autolog()

with open('/workspaces/MLOps-Tut/params.yaml', 'r') as f:
    params = yaml.safe_load(f)

n_estimators = params['model_building']['n_estimators']

train_data = pd.read_csv("/workspaces/MLOps-Tut/data/processed/train_processed.csv")

X_train = train_data.iloc[:,0:-1]
y_train = train_data.iloc[:,-1]

with mlflow.start_run(run_name="RandomForestModel"):
    rf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    rf.fit(X_train, y_train)

    mlflow.log_param("n_estimators", n_estimators)
    
    train_score = rf.score(X_train, y_train)
    print(f"Train Accuracy: {train_score:.3f}")
    
    mlflow.sklearn.log_model(rf, "model")

pickle.dump(rf, open("model.pkl", "wb"))