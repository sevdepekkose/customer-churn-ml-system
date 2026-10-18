from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Customer Churn Prediction API"
    }

sample_customer = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 89.50,
    "TotalCharges": 1074.00
}

def test_predict_valid_customer():

    response = client.post("/predict", json=sample_customer)

    assert response.status_code == 200

    data = response.json()

    assert 0 <= data["churn_probability"] <= 1
    assert data["churn_prediction"] in ["Yes", "No"]
    assert data["threshold"] == 0.30
    expected_prediction = ("Yes" if data["churn_probability"] >= 0.30 else "No")
    assert data["churn_prediction"] == expected_prediction

def test_negative_tenure():
    invalid_customer = sample_customer.copy()

    invalid_customer["tenure"] = -5

    response = client.post("/predict", json=invalid_customer)

    assert response.status_code == 422

def test_invalid_contract():
    invalid_customer = sample_customer.copy()
    invalid_customer["Contract"] = "Random"

    response = client.post("/predict", json=invalid_customer)

    assert response.status_code == 422

def test_valid_online_security():
    valid_customer = sample_customer.copy()
    valid_customer["OnlineSecurity"] = "Yes"

    response = client.post("/predict", json=valid_customer)

    assert response.status_code == 200

def test_inconsistent_internet_service():
    invalid_customer = sample_customer.copy()

    invalid_customer["InternetService"] = "No"

    internet_features = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]

    for feature in internet_features:
        invalid_customer[feature] = "No internet service"

    invalid_customer["OnlineSecurity"] = "Yes"

    response = client.post("/predict", json=invalid_customer)

    assert response.status_code == 422

def test_missing_contract():
    invalid_sample = sample_customer.copy()
    invalid_sample.pop("Contract", None)
    response = client.post("/predict", json=invalid_sample)
    assert response.status_code == 422



    