import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL_PATH = os.path.join(BASE_DIR, "myapp/ml/demand_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "myapp/ml/label_encoders.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "myapp/ml/feature_columns.pkl")

model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)
features = joblib.load(FEATURE_PATH)


def predict_demand(data):

    df = pd.DataFrame([data])

    for column, encoder in encoders.items():

        if column in df.columns:

            value = df[column][0]

            if value not in encoder.classes_:

                value = encoder.classes_[0]

            df[column] = encoder.transform([value])

    prediction = model.predict(df[features])

    return round(float(prediction[0]), 2)