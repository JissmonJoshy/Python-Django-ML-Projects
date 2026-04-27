import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
import os

# =========================
# 1. Load Dataset
# =========================
# Make sure the CSV path is correct
DATA_PATH = "PCOS_data.csv"

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError("PCOS_data.csv not found in project folder")

data = pd.read_csv(DATA_PATH)

# =========================
# 2. Clean Column Names (remove spaces)
# =========================
data.columns = data.columns.str.strip()

# Rename required columns (match your Django form fields)
data = data.rename(columns={
    'Age (yrs)': 'age',
    'Cycle length(days)': 'cycle_length',
    'BMI': 'bmi',
    'Pimples(Y/N)': 'acne',
    'Hair loss(Y/N)': 'hairfall',
    'Weight gain(Y/N)': 'weight_gain',
    'PCOS (Y/N)': 'pcos'
})

# =========================
# 3. Select Required Columns Only
# (Prevents model mismatch errors)
# =========================
required_columns = [
    'age', 'cycle_length', 'bmi',
    'acne', 'hairfall', 'weight_gain', 'pcos'
]

# Drop rows with missing important values
data = data[required_columns].dropna()

# =========================
# 4. Convert Y/N or Yes/No to 0/1 safely
# =========================
binary_cols = ['acne', 'hairfall', 'weight_gain', 'pcos']

for col in binary_cols:
    data[col] = data[col].replace({
        'Y': 1, 'N': 0,
        'Yes': 1, 'No': 0,
        1: 1, 0: 0
    })
    data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0).astype(int)

# =========================
# 5. Features & Target (MUST match Django input)
# =========================
X = data[['age', 'cycle_length', 'bmi', 'acne', 'hairfall', 'weight_gain']]
y = data['pcos']

# Ensure numeric types
X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
y = pd.to_numeric(y, errors='coerce').fillna(0).astype(int)

# =========================
# 6. Train Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# =========================
# 7. Train Model (Stable for small medical dataset)
# =========================
model = LogisticRegression(
    max_iter=2000,
    solver='liblinear',  # more stable
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# 8. Model Accuracy (Optional)
# =========================
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# =========================
# 9. Save Model (Django Compatible)
# =========================
MODEL_PATH = "pcos_model.pkl"
joblib.dump(model, MODEL_PATH)

print("✅ PCOS model trained and saved successfully as pcos_model.pkl")