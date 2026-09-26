import os
import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csv_path = os.path.join(
    BASE_DIR,
    "dataset",
    "football_master_dataset.csv"
)

df = pd.read_csv(csv_path)

FEATURES = [

'overall_rating',

'potential',

'pace',

'shooting',

'passing',

'dribbling',

'defending',

'physical',

'age'

]

X = df[FEATURES]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

knn = NearestNeighbors(
    n_neighbors=6,
    metric="euclidean"
)

knn.fit(X_scaled)

model_folder = os.path.join(
    BASE_DIR,
    "ml_models"
)

os.makedirs(model_folder, exist_ok=True)

joblib.dump(
    knn,
    os.path.join(
        model_folder,
        "knn_model.pkl"
    )
)

joblib.dump(
    scaler,
    os.path.join(
        model_folder,
        "knn_scaler.pkl"
    )
)

joblib.dump(
    FEATURES,
    os.path.join(
        model_folder,
        "knn_features.pkl"
    )
)

print("KNN Model Saved Successfully")