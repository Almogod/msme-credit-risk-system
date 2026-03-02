import shap
from fastapi import APIRouter
from apps.api.schemas.request import LoanRequest
from apps.api.dependencies.model_loader import model_loader

router = APIRouter()

explainer = shap.Explainer(model_loader.pd_model)

@router.post("/")
def explain(data: LoanRequest):
    features = [[
        data.income,
        data.loan_amount,
        data.credit_score,
        data.debt_to_income
    ]]

    shap_values = explainer(features)

    return {
        "explanations": shap_values.values.tolist()
    }
