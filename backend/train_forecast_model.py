from sklearn.linear_model import LinearRegression
import numpy as np
import joblib

X = np.array([
    [100],
    [150],
    [200],
    [250],
    [300],
    [350],
    [400]
])

y = np.array([
    70,
    105,
    140,
    175,
    210,
    245,
    280
])

model = LinearRegression()

model.fit(X, y)

joblib.dump(
    model,
    "forecast_model.pkl"
)

print("Forecast model trained")