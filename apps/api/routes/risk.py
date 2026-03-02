from fastapi import APIRouter
from apps.api.schemas.request import LoanRequest
from apps.api.schemas.response import RiskResponse
from apps.api.dependencies.model_loader import model_loader
from features.build_features import build_features
import pandas as pd

router = APIRouter()

# 1. Use 'def' for CPU-bound ML tasks to avoid blocking the event loop
@router.post("/predict", response_model=RiskResponse)
def predict_risk(data: LoanRequest):
    # 2. Convert Pydantic model to DataFrame for preprocessing
    # Using [data.model_dump()] (Pydantic v2) or [data.dict()] (v1)
    df = pd.DataFrame([data.model_dump()])
    
    # 3. Apply your feature engineering pipeline
    df_transformed = build_features(df)

    # 4. Get probability of class 1 (High Risk)
    # Ensure model_loader is pre-loaded via FastAPI Lifespan to prevent I/O delays
    pd_value = float(model_loader.pd_model.predict_proba(df_transformed)[0][1])

    # 5. Define risk bands based on probability
    if pd_value > 0.7:
        band = "High Risk"
    elif pd_value > 0.4:
        band = "Medium Risk"
    else:
        band = "Low Risk"

    return {"pd": pd_value, "risk_band": band}
