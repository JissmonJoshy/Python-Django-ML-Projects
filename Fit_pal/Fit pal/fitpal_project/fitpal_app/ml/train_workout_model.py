import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv(r'C:\Users\jissj\Desktop\LCC\Depaul(python 25-26)\Fit pal\Fit pal\fitpal_project\gym_members_exercise_tracking_with_plan.csv')

# Drop rows with missing target
df = df.dropna(subset=['Workout_Type'])

# Features for prediction
features = [
    'Age', 'Gender', 'Weight (kg)', 'Height (m)',
    'BMI', 'Fat_Percentage',
    'Workout_Frequency (days/week)', 'Experience_Level'
]

# Drop any rows with missing features
df = df[features + ['Workout_Type', 'Exercise_Plan']].dropna()

# Encode categorical features
le_gender = LabelEncoder()
le_workout = LabelEncoder()

df['Gender'] = le_gender.fit_transform(df['Gender'])
df['Workout_Type'] = le_workout.fit_transform(df['Workout_Type'])

X = df[features]
y = df['Workout_Type']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Save model & encoders
pickle.dump(model, open('workout_model.pkl', 'wb'))
pickle.dump(le_gender, open('gender_encoder.pkl', 'wb'))
pickle.dump(le_workout, open('workout_encoder.pkl', 'wb'))

# Save exercise plan mapping
exercise_plan_mapping = dict(zip(df['Workout_Type'], df['Exercise_Plan']))
pickle.dump(exercise_plan_mapping, open('exercise_plan_mapping.pkl', 'wb'))

print("✅ Workout Recommendation Model Trained & Saved with Exercise Plans")