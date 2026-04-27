# myapp/ml/train_model.py
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Path helpers (run this from project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # points to project root if run via python myapp/ml/train_model.py
# simpler: assume current working directory is project root
PROJECT_ROOT = os.getcwd()

DATA_XLSX = os.path.join(PROJECT_ROOT, "myapp", "ml", "crop_data.xlsx")
DATA_CSV = os.path.join(PROJECT_ROOT, "myapp", "ml", "crop_data.csv")
MODEL_PATH = os.path.join(PROJECT_ROOT, "myapp", "ml", "trained_model.pkl")

# Load dataset (prefer xlsx if exists, else csv)
if os.path.exists(DATA_XLSX):
    df = pd.read_excel(DATA_XLSX, engine="openpyxl")
elif os.path.exists(DATA_CSV):
    df = pd.read_csv(DATA_CSV)
else:
    raise FileNotFoundError("No crop_data.xlsx or crop_data.csv found in myapp/ml/")

# Quick data sanity check — ensure columns exist
expected = {"temperature", "humidity", "rainfall", "crop"}
if not expected.issubset(set(df.columns)):
    raise ValueError(f"Dataset must contain columns: {expected}. Found: {list(df.columns)}")

# Features and target
X = df[["temperature", "humidity", "rainfall"]]
y = df["crop"]

# Optional: encode target if needed (sklearn will accept string labels directly for many classifiers)
# Split (optional — for evaluation)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model — Random Forest for better baseline
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate (print a simple score)
score = model.score(X_test, y_test)
print(f"Validation accuracy: {score:.3f}")

# Save model
joblib.dump(model, MODEL_PATH)
print(f"Model saved to: {MODEL_PATH}")
