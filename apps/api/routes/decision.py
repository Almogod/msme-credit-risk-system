from fastapi import APIRouter
from apps.api.schemas.request import LoanRequest
from apps.api.schemas.response import DecisionResponse
from apps.api.dependencies.model_loader import model_loader

router = APIRouter()

@router.post("/")
def make_decision(data: LoanRequest):
    features = [[
        data.income,
        data.loan_amount,
        data.credit_score,
        data.debt_to_income
    ]]

    pd = model_loader.pd_model.predict_proba(features)[0][1]

    if pd > 0.7:
        return {"decision": "Rejected", "reason": "High default risk"}
    elif pd > 0.4:
        return {"decision": "Conditional Approval", "reason": "Moderate risk"}
    else:
        return {"decision": "Approved", "reason": "Low risk"}
