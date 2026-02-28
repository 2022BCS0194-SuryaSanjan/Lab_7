import os
import joblib
import numpy as np
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

model_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "artifacts",
        "model.pkl"
    )
)

model = joblib.load(model_path)

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")

@app.get("/predict")
def predict(
    fixed_acidity: float,
    volatile_acidity: float,
    citric_acid: float,
    residual_sugar: float,
    chlorides: float,
    free_sulfur_dioxide: float,
    total_sulfur_dioxide: float,
    density: float,
    ph: float,
    sulphates: float,
    alcohol: float
):
    features = np.array([[
        fixed_acidity,
        volatile_acidity,
        citric_acid,
        residual_sugar,
        chlorides,
        free_sulfur_dioxide,
        total_sulfur_dioxide,
        density,
        ph,
        sulphates,
        alcohol
    ]])

    prediction = model.predict(features)

    return {
        "name": "Yeshwanth",
        "roll_no": "2022bcd0056",
        "wine_quality": int(round(prediction[0]))
    }
