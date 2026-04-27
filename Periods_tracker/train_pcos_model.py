import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# sample dataset
data = pd.read_csv('pcos_dataset1.csv')

X = data[['age','cycle_length','delay_days','acne','hairfall','bmi']]
y_reason = data['reason']        # PCOS / Stress / Hormonal
y_pcos = data['pcos']            # 0 or 1

# train models
reason_model = DecisionTreeClassifier()
pcos_model = DecisionTreeClassifier()

reason_model.fit(X, y_reason)
pcos_model.fit(X, y_pcos)

# save models
joblib.dump(reason_model, 'reason_model.pkl')
joblib.dump(pcos_model, 'pcos_model.pkl')
