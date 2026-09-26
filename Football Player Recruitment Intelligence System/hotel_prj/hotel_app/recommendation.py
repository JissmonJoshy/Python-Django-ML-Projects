import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csv_path = os.path.join(
    BASE_DIR,
    "dataset",
    "football_master_dataset.csv"
)

df = pd.read_csv(csv_path)

knn = joblib.load(
    os.path.join(
        BASE_DIR,
        "ml_models",
        "knn_model.pkl"
    )
)

scaler = joblib.load(
    os.path.join(
        BASE_DIR,
        "ml_models",
        "knn_scaler.pkl"
    )
)

FEATURES = joblib.load(
    os.path.join(
        BASE_DIR,
        "ml_models",
        "knn_features.pkl"
    )
)


def similar_players(player_name):

    player = df[df["name"] == player_name]

    if player.empty:
        return None

    player_features = scaler.transform(
        player[FEATURES]
    )

    distances, indices = knn.kneighbors(
        player_features
    )

    recommendations = []

    for i in indices[0][1:]:

        recommendations.append({

            "name": df.iloc[i]["name"],

            "club": df.iloc[i]["club"],

            "position": df.iloc[i]["position"],

            "overall": df.iloc[i]["overall_rating"],

            "market_value": df.iloc[i]["market_value_eur"]

        })

    return recommendations


