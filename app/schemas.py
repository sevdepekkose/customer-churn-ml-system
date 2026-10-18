from pydantic import BaseModel, Field, model_validator
from typing import Literal

class CustomerRequest(BaseModel):
    gender: Literal["Male", "Female"]
    SeniorCitizen: Literal[0,1]
    Partner: Literal["Yes", "No"]
    Dependents: Literal["Yes", "No"]
    tenure: int = Field(ge=0)
    PhoneService: Literal["Yes", "No"]
    MultipleLines: Literal["Yes", "No","No phone service"]
    InternetService: Literal["Fiber optic","DSL","No"]
    OnlineSecurity: Literal["Yes", "No","No internet service"]
    OnlineBackup: Literal["Yes", "No","No internet service"]
    DeviceProtection: Literal["Yes", "No","No internet service"]
    TechSupport: Literal["Yes", "No","No internet service"]
    StreamingTV: Literal["Yes", "No","No internet service"]
    StreamingMovies:Literal["Yes", "No","No internet service"]
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: Literal["Yes", "No"]
    PaymentMethod: Literal["Electronic check","Mailed check","Bank transfer (automatic)", "Credit card (automatic)"]
    MonthlyCharges: float =Field(ge=0)
    TotalCharges: float =Field(ge=0)

    @model_validator(mode="after")
    def validate_services(self):

        # Telefon hizmeti kontrolü
        if self.PhoneService == "No":
            if self.MultipleLines != "No phone service":
                raise ValueError(
                    "MultipleLines must be 'No phone service' when PhoneService is 'No'"
                )

        # İnternet hizmetine bağlı özellikler
        internet_features = [
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies"
        ]

        for feature in internet_features:
            value = getattr(self, feature)

            if self.InternetService == "No":
                if value != "No internet service":
                    raise ValueError(
                        f"{feature} must be 'No internet service' when InternetService is 'No'"
                    )
            else:
                if value == "No internet service":
                    raise ValueError(
                        f"{feature} cannot be 'No internet service' when InternetService is available"
                    )

        return self
    
