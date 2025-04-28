import pandas as pd
import numpy as np
import os
import json
import pickle
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from dvclive import Live

test_data = pd.read_csv('/workspaces/MLOps-Tut/data/processed/train_processed.csv')

X_test = test_data.iloc[:,0:-1].values  # Reverse the rows of the DataFrame
y_test = test_data.iloc[:, -1].values

model = pickle.load(open('/workspaces/MLOps-Tut/model.pkl', 'rb'))

y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

with Live(save_dvc_exp = True) as live:
    live.log("accuracy", acc)
    live.log("precision", precision)
    live.log("recall", recall)
    live.log("f1_score", f1)
    live.log("classification_report", report)


metrics = {
    'accuracy': acc,
    'precision': precision,
    'recall': recall,
    'f1_score': f1,
    'classification_report': report
}

with open('/workspaces/MLOps-Tut/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=4)

