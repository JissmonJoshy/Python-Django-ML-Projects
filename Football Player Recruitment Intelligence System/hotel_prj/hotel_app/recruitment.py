import os
import joblib
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

scaler = joblib.load(
    os.path.join(
        BASE_DIR,
        "ml_models",
        "recruitment_scaler.pkl"
    )
)

FEATURES = joblib.load(
    os.path.join(
        BASE_DIR,
        "ml_models",
        "recruitment_features.pkl"
    )
)

df = joblib.load(
    os.path.join(
        BASE_DIR,
        "ml_models",
        "recruitment_data.pkl"
    )
)


def recommend_players(position, max_age, min_rating):

    filtered = df[
        (df["position"] == position) &
        (df["age"] <= max_age) &
        (df["overall_rating"] >= min_rating)
    ]

    if filtered.empty:
        return []

    X = scaler.transform(filtered[FEATURES])

    # Ideal player profile
    ideal = [[
        95,   # overall_rating
        95,   # potential
        22,   # age
        90,   # pace
        90,   # shooting
        90,   # passing
        90,   # dribbling
        80,   # defending
        85    # physical
    ]]

    ideal_scaled = scaler.transform(pd.DataFrame(ideal, columns=FEATURES))

    similarity = cosine_similarity(X, ideal_scaled)

    filtered = filtered.copy()
    filtered["score"] = similarity

    filtered = filtered.sort_values(
        by="score",
        ascending=False
    )

    return filtered.head(10)[[
        "name",
        "club",
        "position",
        "age",
        "overall_rating",
        "market_value_eur",
        "score"
    ]].to_dict("records")