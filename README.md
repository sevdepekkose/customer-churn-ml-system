# Customer Churn Prediction System

## Project Overview

This project aims to predict customer churn in a telecommunications
company using machine learning.

A Logistic Regression model is trained on the IBM Telco Customer
Churn dataset to estimate the probability of customer churn.

The system provides a Streamlit web interface connected to a
FastAPI backend, allowing users to enter customer information
and receive churn predictions.

## Dataset

This project uses the IBM Telco Customer Churn dataset, which
contains information about telecommunications customers and
whether they have churned.

- Original dataset: 7,043 customers
- Dataset after cleaning: 7,032 customers
- Input features: 19
- Target variable: Churn (Yes / No)
- Problem type: Binary classification
- Train/test split: 80% / 20% (stratified)

The dataset includes customer demographics, subscription
details, service usage, and billing information.

During data cleaning, 11 records with missing TotalCharges
values were removed.

## Machine Learning Pipeline

The machine learning pipeline consists of the following steps:

1. **Data Preprocessing**
   - StandardScaler for numerical features
   - OneHotEncoder for categorical features
   - ColumnTransformer to combine preprocessing steps

2. **Model Training**
   - Logistic Regression classifier
   - Scikit-learn Pipeline for preprocessing and prediction

3. **Model Evaluation**
   - Stratified 5-fold cross-validation
   - Precision, recall, and F1-score
   - Confusion matrix

4. **Decision Threshold Selection**
   - Different classification thresholds were evaluated.
   - A threshold of 0.30 was selected based on
     out-of-fold F1-score.
   - The selected threshold prioritizes identifying
     more potential churners at the cost of additional
     false positives.

## Model Performance

The Logistic Regression model was evaluated on the test set
using a decision threshold of 0.30.

| Metric | Score |
|--------|-------|
| Precision | 0.511 |
| Recall | 0.759 |
| F1-score | 0.611 |
| Decision Threshold | 0.30 |

### Confusion Matrix

| | Predicted No | Predicted Yes |
|---|---:|---:|
| Actual No | 761 | 272 |
| Actual Yes | 90 | 284 |

The model prioritizes recall to identify a larger proportion
of customers who may churn.

This comes at the cost of more false positives, which could
lead to unnecessary customer retention efforts.

The decision threshold can be adjusted depending on business
requirements and the relative costs of false positives and
false negatives.


## System Architecture

The application consists of two services:

- **Streamlit:** Provides an interactive interface for entering
  customer information and displaying predictions.
- **FastAPI:** Validates customer data, loads the trained model,
  and returns churn predictions.

### Prediction Flow

1. The user enters customer information in Streamlit.
2. Streamlit sends a POST request to the FastAPI backend.
3. FastAPI validates the input using Pydantic.
4. The ML pipeline preprocesses the data and calculates
   the churn probability.
5. The probability is compared with the decision threshold.
6. The prediction is returned to Streamlit and displayed.

Both services are containerized using Docker and orchestrated
with Docker Compose.

## Getting Started

### Prerequisites

- Git
- Docker
- Docker Compose

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sevdepekkose/customer-churn-ml-system.git
   ```

2. Navigate to the project directory:

   ```bash
   cd customer-churn-ml-system
   ```

3. Build and start the application:

   ```bash
   docker compose up --build
   ```

4. Open the application:

   - Streamlit UI: http://localhost:8501
   - FastAPI Documentation: http://localhost:8000/docs

5. Enter customer information and click **Predict Churn**
   to generate a prediction.

### Stopping the Application

Press `Ctrl+C` in the terminal.

To remove the containers and Compose network, run:

```bash
docker compose down
```

## API Endpoints

The FastAPI backend provides the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Returns a welcome message |
| GET | `/model-info` | Returns model information and decision threshold |
| POST | `/predict` | Generates a customer churn prediction |

### Example Prediction Response

```json
{
  "churn_probability": 0.65,
  "churn_prediction": "Yes",
  "threshold": 0.3
}
```

The prediction response contains:

- **churn_probability:** Estimated probability of customer churn.
- **churn_prediction:** Predicted class (Yes or No).
- **threshold:** Decision threshold used for classification.

The `/predict` endpoint accepts customer information in JSON
format and validates the input using Pydantic.

Interactive API documentation is available at:

http://localhost:8000/docs

## Project Structure

```text
customer-churn-ml-system/
│
├── app/
│   ├── main.py
│   └── schemas.py
│
├── frontend/
│   └── streamlit_app.py
│
├── models/
│   ├── churn_model.joblib
│   └── model_config.joblib
│
├── notebooks/
│   └── ...
│
├── tests/
│   └── test_api.py
│
├── Dockerfile.api
├── Dockerfile.streamlit
├── compose.yaml
├── requirements.txt
├── .gitignore
├── .dockerignore
└── README.md
```

### Main Components

- `app/main.py`: FastAPI application and prediction endpoints.
- `app/schemas.py`: Input validation using Pydantic.
- `frontend/streamlit_app.py`: Interactive prediction interface.
- `models/`: Trained ML pipeline and model configuration.
- `notebooks/`: Data exploration, model development, and evaluation.
- `tests/`: Automated API tests.
- `Dockerfile.api`: Docker configuration for the backend.
- `Dockerfile.streamlit`: Docker configuration for the frontend.
- `compose.yaml`: Multi-container orchestration.


## Limitations and Future Improvements

### Limitations

- The model was trained on a historical, cross-sectional
  telecommunications dataset. Predictions represent patterns
  learned from this dataset and do not establish causality.

- The dataset may not represent the customer population of
  other telecommunications companies.

- The classification threshold was selected using out-of-fold
  predictions. Its performance may vary on new data.

- The test set was inspected during model development.
  Therefore, the reported test metrics should not be
  interpreted as a completely untouched final evaluation.

- The model's predicted probabilities have not been
  independently evaluated for calibration.

### Future Improvements

- Evaluate the model on a new, independent test dataset.
- Compare Logistic Regression with tree-based models.
- Investigate probability calibration.
- Incorporate business costs into threshold selection.
- Add model monitoring and data drift detection.
- Deploy the application to a cloud platform.