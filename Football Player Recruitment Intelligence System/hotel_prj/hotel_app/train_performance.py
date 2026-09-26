import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csv_path = os.path.join(
    BASE_DIR,
    "dataset",
    "football_master_dataset.csv"
)

df = pd.read_csv(csv_path)

FEATURES = [

'age',

'height_cm',

'weight_kg',

'pace',

'shooting',

'passing',

'dribbling',

'defending',

'physical',

'crossing',

'finishing',

'short_passing',

'long_passing',

'vision',

'ball_control',

'stamina',

'strength',

'aggression',

'interceptions',

'matches_played',

'minutes_played',

'goals',

'assists'

]

TARGET = "overall_rating"

X = df[FEATURES]

y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

model = RandomForestRegressor(

    n_estimators=300,

    random_state=42

)

model.fit(X_train, y_train)

prediction = model.predict(X_test)

print()

print("R2 Score :", r2_score(y_test, prediction))

print("MAE :", mean_absolute_error(y_test, prediction))

model_folder = os.path.join(

    BASE_DIR,

    "ml_models"

)

os.makedirs(

    model_folder,

    exist_ok=True

)

joblib.dump(

    model,

    os.path.join(

        model_folder,

        "performance_model.pkl"

    )

)

joblib.dump(

    FEATURES,

    os.path.join(

        model_folder,

        "performance_features.pkl"

    )

)

print()

print("Performance Model Saved Successfully")
