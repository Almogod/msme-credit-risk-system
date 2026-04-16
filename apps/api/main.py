from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

app = FastAPI(title="MSME Credit Risk API")

class LoanRequest(BaseModel):
    age_years: int
    employees: int
    is_franchise: int
    urban_rural: int
    annual_revenue: float
    net_profit: float
    fixed_assets: float
    inventory_value: float
    total_assets: float
    valuation: float
    existing_debt: float
    requested_amount: float

# Globals to store models
MODELS = {}

@app.on_event("startup")
def load_models():
    """Load models on startup."""
    try:
        MODELS['classifier'] = joblib.load("models/saved/classifier.joblib")
        MODELS['regressor'] = joblib.load("models/saved/regressor.joblib")
        MODELS['pipeline'] = joblib.load("models/saved/pipeline.joblib")
        MODELS['explainer'] = joblib.load("models/saved/explainer.joblib")
        print("Models and SHAP explainer loaded successfully.")
    except Exception as e:
        print(f"Error loading models: {e}. Ensure training is done.")

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
def predict(request: LoanRequest):
    if not MODELS:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    # Convert request to DataFrame
    input_df = pd.DataFrame([request.dict()])
    
    # Transform
    features = MODELS['pipeline'].transform(input_df)
    
    # Approval Prediction
    prob_paid = float(MODELS['classifier'].predict_proba(features)[0][1])
    approved = prob_paid > 0.7 # Threshold for approval
    
    # SHAP Explainability
    shap_values = MODELS['explainer'].shap_values(features)
    # SHAP values for the 'Paid' class (index 1)
    feature_importance = dict(zip(features.columns, shap_values[0].tolist()))
    
    # Limit Prediction
    recommended_limit = float(MODELS['regressor'].predict(features)[0])
    
    # Asset-based max loan (Valuation Logic)
    valuation_cap = request.valuation * 0.4 - request.existing_debt
    asset_cap = request.fixed_assets * 0.8 - request.existing_debt
    max_loan_cap = max(valuation_cap, asset_cap, 0)
    
    # Final Recommendation
    final_limit = min(recommended_limit, max_loan_cap)
    
    return {
        "approval_probability": prob_paid,
        "is_approved": approved,
        "recommended_limit": recommended_limit,
        "max_allowable_loan": max_loan_cap,
        "final_loan_recommendation": final_limit if approved else 0,
        "feature_importance": feature_importance,
        "remarks": "Loan approved based on cash flow and asset valuation." if approved else "Loan rejected due to high risk profile."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
