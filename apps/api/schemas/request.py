from pydantic import BaseModel

class LoanRequest(BaseModel):
    income: float
    loan_amount: float
    credit_score: float
    debt_to_income: float
    assets: float
    revenue: float
