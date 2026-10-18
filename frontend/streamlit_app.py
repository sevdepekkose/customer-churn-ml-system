import streamlit as st
import os
import requests

st.title("Customer Churn Prediction System")

st.write(
    "Enter customer information to predict the probability of churn."
)

# Customer information
st.subheader("Customer Information")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Female", "Male"])

    senior_citizen = st.selectbox("Senior Citizen", [0, 1])

    partner = st.selectbox("Partner", ["Yes", "No"])

    dependents = st.selectbox("Dependents", ["Yes", "No"])

    tenure = st.number_input(
        "Tenure (months)",
        min_value=0,
        value=12
    )

with col2:
    contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
    )

    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.0
    )

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=840.0
    )


# Phone services
st.subheader("Phone Services")

col3, col4 = st.columns(2)

with col3:
    phone_service = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

with col4:
    if phone_service == "Yes":
        multiple_lines = st.selectbox(
            "Multiple Lines",
            ["Yes", "No"]
        )
    else:
        multiple_lines = "No phone service"
        st.info("Multiple Lines: No phone service")


# Internet services
st.subheader("Internet Services")

internet_service = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)

if internet_service == "No":

    online_security = "No internet service"
    online_backup = "No internet service"
    device_protection = "No internet service"
    tech_support = "No internet service"
    streaming_tv = "No internet service"
    streaming_movies = "No internet service"

    st.info("Internet-related services are unavailable.")

else:

    col5, col6 = st.columns(2)

    with col5:
        online_security = st.selectbox(
            "Online Security",
            ["Yes", "No"]
        )

        online_backup = st.selectbox(
            "Online Backup",
            ["Yes", "No"]
        )

        device_protection = st.selectbox(
            "Device Protection",
            ["Yes", "No"]
        )

    with col6:
        tech_support = st.selectbox(
            "Tech Support",
            ["Yes", "No"]
        )

        streaming_tv = st.selectbox(
            "Streaming TV",
            ["Yes", "No"]
        )

        streaming_movies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No"]
        )

customer_data = {
    "gender": gender,
    "SeniorCitizen": senior_citizen,
    "Partner": partner,
    "Dependents": dependents,
    "tenure": tenure,
    "PhoneService": phone_service,
    "MultipleLines": multiple_lines,
    "InternetService": internet_service,
    "OnlineSecurity": online_security,
    "OnlineBackup": online_backup,
    "DeviceProtection": device_protection,
    "TechSupport": tech_support,
    "StreamingTV": streaming_tv,
    "StreamingMovies": streaming_movies,
    "Contract": contract,
    "PaperlessBilling": paperless_billing,
    "PaymentMethod": payment_method,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges
}

if st.button("Predict Churn"):

    try:
        response = requests.post(
            f"{os.getenv('API_URL', 'http://127.0.0.1:8000')}/predict",
            json=customer_data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()

            probability = result["churn_probability"]
            prediction = result["churn_prediction"]
            threshold = result["threshold"]

            st.subheader("Prediction Result")

            st.metric(
                label="Churn Probability",
                value=f"{probability:.1%}"
            )

            st.progress(probability)

            st.write(f"Decision Threshold: {threshold:.0%}")

            if prediction == "Yes":
                st.warning("Customer is predicted to churn.")
            else:
                st.success("Customer is predicted to stay.")

        else:
            st.error(f"Prediction failed: HTTP {response.status_code}")

    except requests.exceptions.RequestException:
        st.error("Cannot connect to the prediction API.")