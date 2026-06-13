from sklearn.ensemble import RandomForestRegressor
import numpy as np
import joblib

X = np.array([
    [50, 8],
    [100, 6],
    [150, 4],
    [200, 2],
    [250, 1],
    [300, 1],
    [80, 12],
    [120, 10],
    [180, 3],
    [220, 2]
])

y = np.array([
    40,
    55,
    75,
    95,
    110,
    120,
    35,
    50,
    90,
    105
])

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(
    model,
    "priority_model.pkl"
)

print("Priority model trained successfully")