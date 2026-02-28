import pandas as pd
import json
import math
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
data = pd.read_csv("data/wine+quality/winequality-red.csv", sep=";")

X = data.drop("quality", axis=1)
y = data["quality"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(
    random_state=42,
    n_estimators=50,
    max_depth=8
)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Metrics
rmse = math.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse}")
print(f"R2 Score: {r2}")

# Save model
joblib.dump(model, "model.pkl")

# Save metrics
metrics = {
    "rmse": rmse,
    "r2": r2
}

with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)
