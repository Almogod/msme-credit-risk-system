from pydantic import BaseModel

class RiskResponse(BaseModel):
    pd: float
    risk_band: str

class DecisionResponse(BaseModel):
    decision: str
    reason: str

class CreditResponse(BaseModel):
    credit_limit: float
