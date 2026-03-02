from fastapi import APIRouter
from apps.api.schemas.request import LoanRequest
from apps.api.schemas.response import RiskResponse
from apps.api.dependencies.model_loader import model_loader

router = APIRouter()

@router.post("/predict", response_model=RiskResponse)
def predict_risk(data: LoanRequest):
    features = [[
        data.income,
        data.loan_amount,
        data.credit_score,
        data.debt_to_income
    ]]

    pd = model_loader.pd_model.predict_proba(features)[0][1]

    if pd > 0.7:
        band = "High Risk"
    elif pd > 0.4:
        band = "Medium Risk"
    else:
        band = "Low Risk"

    return {"pd": pd, "risk_band": band}
