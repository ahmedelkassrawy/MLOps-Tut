from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import pickle
from sklearn.metrics import accuracy_score, classification_report

train_data = pd.read_csv("/workspaces/MLOps-Tut/data/processed/train_processed.csv")

X_train = train_data.iloc[:,0:-1].values
y_train = train_data.iloc[:,-1].values

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

pickle.dump(rf, open("model.pkl", "wb"))