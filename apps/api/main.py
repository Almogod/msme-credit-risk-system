from fastapi import FastAPI
from apps.api.routes import risk, decision, credit, explain

app = FastAPI(title="Loan Risk System API")

app.include_router(risk.router, prefix="/risk", tags=["Risk"])
app.include_router(decision.router, prefix="/decision", tags=["Decision"])
app.include_router(credit.router, prefix="/credit", tags=["Credit"])
app.include_router(explain.router, prefix="/explain", tags=["Explain"])
