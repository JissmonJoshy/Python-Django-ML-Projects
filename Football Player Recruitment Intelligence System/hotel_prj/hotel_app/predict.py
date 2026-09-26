import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(
    os.path.join(
        BASE_DIR,
        "ml_models",
        "performance_model.pkl"
    )
)

FEATURES = joblib.load(
    os.path.join(
        BASE_DIR,
        "ml_models",
        "performance_features.pkl"
    )
)

csv_path = os.path.join(
    BASE_DIR,
    "dataset",
    "football_master_dataset.csv"
)

df = pd.read_csv(csv_path)


def predict_player(player_name):

    player = df[df["name"] == player_name]

    if player.empty:
        return None

    X = player[FEATURES]

    prediction = model.predict(X)[0]

    player = player.iloc[0]

    return {

        "player_name": player["name"],

        "club": player["club"],

        "nationality": player["nationality"],

        "age": player["age"],

        "position": player["position"],

        "overall_rating": player["overall_rating"],

        "predicted_rating": round(prediction,2),

        "potential": player["potential"],

        "pace": player["pace"],

        "shooting": player["shooting"],

        "passing": player["passing"],

        "dribbling": player["dribbling"],

        "defending": player["defending"],

        "physical": player["physical"],

        "goals": player["goals"],

        "assists": player["assists"],

        "market_value": player["market_value_eur"]

    }