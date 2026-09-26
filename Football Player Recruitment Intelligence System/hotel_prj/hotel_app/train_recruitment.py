import os
import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csv_path = os.path.join(
    BASE_DIR,
    "dataset",
    "football_master_dataset.csv"
)

df = pd.read_csv(csv_path)

FEATURES = [

    "overall_rating",
    "potential",
    "age",
    "pace",
    "shooting",
    "passing",
    "dribbling",
    "defending",
    "physical"

]

X = df[FEATURES]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

model_folder = os.path.join(
    BASE_DIR,
    "ml_models"
)

os.makedirs(model_folder, exist_ok=True)

joblib.dump(
    scaler,
    os.path.join(
        model_folder,
        "recruitment_scaler.pkl"
    )
)

joblib.dump(
    FEATURES,
    os.path.join(
        model_folder,
        "recruitment_features.pkl"
    )
)

joblib.dump(
    df,
    os.path.join(
        model_folder,
        "recruitment_data.pkl"
    )
)

print("--------------------------------")
print("Recruitment Recommendation Ready")
print("--------------------------------")
print("Players :", len(df))
print("Features :", FEATURES)
print("--------------------------------")