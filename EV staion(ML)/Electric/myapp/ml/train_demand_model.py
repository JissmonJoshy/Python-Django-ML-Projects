import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# ----------------------------------------------------
# Dataset Path
# ----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

csv_path = os.path.join(
    BASE_DIR,
    "dataset",
    "ev_charging_dataset.csv"
)

print("Loading Dataset...")
df = pd.read_csv(csv_path)

print(df.head())

# ----------------------------------------------------
# Remove Missing Values
# ----------------------------------------------------

df = df.dropna()

# ----------------------------------------------------
# Features
# ----------------------------------------------------

FEATURES = [

    "station_id",

    "location_type",

    "vehicle_type",

    "charging_power_kW",

    "queue_length",

    "station_load",

    "electricity_price",

    "renewable_energy_ratio",

    "traffic_density",

    "weather_condition",

    "day_of_week",

    "time_slot"

]

TARGET = "charging_demand"

# ----------------------------------------------------
# Encode Categorical Columns
# ----------------------------------------------------

label_encoders = {}

for col in FEATURES:

    if df[col].dtype == "object":

        encoder = LabelEncoder()

        df[col] = encoder.fit_transform(df[col])

        label_encoders[col] = encoder

# ----------------------------------------------------
# Prepare Data
# ----------------------------------------------------

X = df[FEATURES]

y = df[TARGET]

# ----------------------------------------------------
# Train Test Split
# ----------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.20,
    random_state=42

)

# ----------------------------------------------------
# Train Model
# ----------------------------------------------------

print("Training Random Forest...")

model = RandomForestRegressor(

    n_estimators=300,
    random_state=42

)

model.fit(X_train, y_train)

# ----------------------------------------------------
# Evaluate
# ----------------------------------------------------

prediction = model.predict(X_test)

print("\nModel Performance")

print("---------------------------")

print("R2 Score :", round(r2_score(y_test, prediction),4))

print("MAE      :", round(mean_absolute_error(y_test,prediction),4))

# ----------------------------------------------------
# Save Files
# ----------------------------------------------------

joblib.dump(model,
            os.path.join(BASE_DIR,"myapp/ml/demand_model.pkl"))

joblib.dump(label_encoders,
            os.path.join(BASE_DIR,"myapp/ml/label_encoders.pkl"))

joblib.dump(FEATURES,
            os.path.join(BASE_DIR,"myapp/ml/feature_columns.pkl"))

print("\nModel Saved Successfully")