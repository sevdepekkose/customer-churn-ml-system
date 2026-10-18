from fastapi import FastAPI
from app.schemas import CustomerRequest
import joblib
import pandas as pd

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(BASE_DIR / "models" / "churn_model.joblib")
config = joblib.load(BASE_DIR / "models" / "model_config.joblib")



app = FastAPI()

@app.get("/")
def home():
    return {"message": "Customer Churn Prediction API"}


@app.get("/model-info")
def model_info():
    return {
        "model_type": type(model).__name__,
        "threshold": config["threshold"]
    }

@app.post("/predict")
def predict(customer: CustomerRequest):

    customer_dict = customer.model_dump()
    customer_df = pd.DataFrame([customer_dict])

    probabilities = model.predict_proba(customer_df)

    churn_probability = probabilities[0][1]

    threshold = config["threshold"]
    
    churn_prediction = "Yes" if churn_probability >= threshold else "No"

    return {
        "churn_probability": float(churn_probability),
        "churn_prediction": churn_prediction,
        "threshold": threshold
    }