import joblib

model = joblib.load("mon_app/ml_model/emotion_model.pkl")

def predict_emotion(text):
    return model.predict([text])[0]