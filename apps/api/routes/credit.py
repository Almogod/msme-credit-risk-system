from fastapi import APIRouter
from apps.api.schemas.request import LoanRequest
from apps.api.schemas.response import CreditResponse
from apps.api.dependencies.model_loader import model_loader

router = APIRouter()

@router.post("/")
def predict_credit(data: LoanRequest):
    features = [[
        data.income,
        data.loan_amount,
        data.credit_score,
        data.debt_to_income
    ]]

    predicted_limit = model_loader.credit_model.predict(features)[0]

    # Business rules
    final_limit = min(
        predicted_limit,
        0.3 * data.revenue,
        0.7 * data.assets
    )

    return {"credit_limit": final_limit}
