import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import numpy as np

# 1. Generate Research Data
np.random.seed(42)
data = []
for i in range(500):
    att = np.random.randint(30, 100)
    study = np.random.randint(0, 20)
    g1 = np.random.randint(30, 95)
    g2 = np.clip(g1 + (att*0.1 + study*0.5 - 10), 0, 100)
    data.append([att, study, g1, g2])

df = pd.DataFrame(data, columns=['Attendance', 'Study_Hours', 'G1', 'G2'])
df['Volatility'] = df['G2'] - df['G1']

# 2. Train Model
X = df[['Attendance', 'Study_Hours', 'G2', 'Volatility']]
y = df['G2'] + (df['Volatility'] * 0.4) 
model = RandomForestRegressor(n_estimators=100).fit(X, y)

# 3. Save
joblib.dump(model, 'pathfinder_model.pkl')
print("✅ Brain Trained and Saved.")