import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csv_path = os.path.join(BASE_DIR, 'data', 'crop_disease.csv')

df = pd.read_csv(csv_path)

le_crop = LabelEncoder()
le_disease = LabelEncoder()

df['Crop'] = le_crop.fit_transform(df['Crop'])
df['Disease'] = le_disease.fit_transform(df['Disease'])

X = df[['Crop', 'Temperature_C', 'Humidity_%', 'Soil_Moisture_%', 'Rainfall_mm']]
y = df['Disease']

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

joblib.dump(model, os.path.join(BASE_DIR, 'ml', 'crop_disease_model.pkl'))
joblib.dump(le_crop, os.path.join(BASE_DIR, 'ml', 'crop_encoder.pkl'))
joblib.dump(le_disease, os.path.join(BASE_DIR, 'ml', 'disease_encoder.pkl'))

print("ML files created successfully")
