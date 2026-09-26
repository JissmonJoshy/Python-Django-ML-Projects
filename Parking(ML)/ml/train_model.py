import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# -----------------------------------
# Load Dataset
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csv_path = os.path.join(
    BASE_DIR,
    "dataset",
    "IIoT_Smart_Parking_Management.csv"
)

df = pd.read_csv(csv_path)


print(df.head())


# -----------------------------------
# Convert Entry Time to Hour
# -----------------------------------

df["Entry_Time"] = df["Entry_Time"].astype(int)


# -----------------------------------
# Select Features
# -----------------------------------

FEATURES = [

    "Parking_Spot_ID",

    "Vehicle_Type",

    "User_Type",

    "Weather_Temperature",

    "Weather_Precipitation",

    "Nearby_Traffic_Level",

    "Electric_Vehicle",

    "Reserved_Status",

    "Parking_Lot_Section",

    "Spot_Size",

    "Proximity_To_Exit",

    "Entry_Time"

]

TARGET = "Occupancy_Status"


df = df[FEATURES + [TARGET]]


# -----------------------------------
# Encode Categorical Columns
# -----------------------------------

encoders = {}

categorical_columns = [

    "Vehicle_Type",

    "User_Type",

    "Nearby_Traffic_Level",

    "Parking_Lot_Section",

    "Spot_Size",

    "Occupancy_Status"

]

for col in categorical_columns:

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col])

    encoders[col] = encoder


# -----------------------------------
# Split Data
# -----------------------------------

X = df[FEATURES]

y = df[TARGET]


X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.20,
    random_state=42

)


# -----------------------------------
# Train Model
# -----------------------------------

model = RandomForestClassifier(

    n_estimators=200,
    random_state=42

)

model.fit(X_train, y_train)


# -----------------------------------
# Prediction
# -----------------------------------

y_pred = model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)


print("\nAccuracy : ", accuracy)

print("\nClassification Report\n")

print(classification_report(y_test, y_pred))


# -----------------------------------
# Save Model
# -----------------------------------

joblib.dump(

    model,

    os.path.join(BASE_DIR, "ml", "occupancy_model.pkl")

)

joblib.dump(

    encoders,

    os.path.join(BASE_DIR, "ml", "occupancy_encoder.pkl")

)

joblib.dump(

    FEATURES,

    os.path.join(BASE_DIR, "ml", "feature_columns.pkl")

)


print("\nModel Saved Successfully")