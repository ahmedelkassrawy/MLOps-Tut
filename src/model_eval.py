import pandas as pd
import numpy as np
import os
import json
import pickle
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from dvclive import Live
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn

test_data = pd.read_csv('/workspaces/MLOps-Tut/data/processed/test_processed.csv')

X_test = test_data.iloc[:,0:-1]  # All columns except the last one
y_test = test_data.iloc[:, -1]   # Only the last column

with mlflow.start_run():
    model = pickle.load(open('/workspaces/MLOps-Tut/model.pkl', 'rb'))

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    
    mlflow.sklearn.log_model(model, "model")

with Live(save_dvc_exp=True) as live:
    live.log_metric("accuracy", acc)
    live.log_metric("precision", precision)
    live.log_metric("recall", recall)
    live.log_metric("f1_score", f1)
    
    cm = confusion_matrix(y_test, y_pred).tolist()
    live.log_artifact("confusion_matrix.json", cm)


metrics = {
    'accuracy': float(acc),
    'precision': float(precision),
    'recall': float(recall),
    'f1_score': float(f1),
    'classification_report': str(report)
}

with open('/workspaces/MLOps-Tut/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=4)

