import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load model
model = joblib.load(
    os.path.join(BASE_DIR, "ml", "occupancy_model.pkl")
)

# Load encoders
encoders = joblib.load(
    os.path.join(BASE_DIR, "ml", "occupancy_encoder.pkl")
)

# Load feature names
FEATURES = joblib.load(
    os.path.join(BASE_DIR, "ml", "feature_columns.pkl")
)


def predict_occupancy(data):

    input_data = data.copy()

    # Encode categorical values

    input_data["Vehicle_Type"] = encoders["Vehicle_Type"].transform(
        [input_data["Vehicle_Type"]]
    )[0]

    input_data["User_Type"] = encoders["User_Type"].transform(
        [input_data["User_Type"]]
    )[0]

    input_data["Nearby_Traffic_Level"] = encoders["Nearby_Traffic_Level"].transform(
        [input_data["Nearby_Traffic_Level"]]
    )[0]

    input_data["Parking_Lot_Section"] = encoders["Parking_Lot_Section"].transform(
        [input_data["Parking_Lot_Section"]]
    )[0]

    input_data["Spot_Size"] = encoders["Spot_Size"].transform(
        [input_data["Spot_Size"]]
    )[0]

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]

    probability = model.predict_proba(df)[0]

    confidence = max(probability) * 100

    prediction = encoders["Occupancy_Status"].inverse_transform(
        [prediction]
    )[0]

    if prediction == "Vacant":

        recommendation = "Parking space is likely available. You can proceed with booking."

    else:

        recommendation = "Parking space is likely occupied. Please choose another slot."

    return prediction, round(confidence, 2), recommendation