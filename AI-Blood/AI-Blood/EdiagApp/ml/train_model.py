import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

data = pd.read_csv("Training.csv")

X = data.drop("Disease", axis=1)
y = data["Disease"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

with open("blood_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved")