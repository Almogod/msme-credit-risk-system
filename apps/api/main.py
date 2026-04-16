from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import sys
from sqlalchemy.orm import Session

# Add project root to path
sys.path.append(os.getcwd())

from services.database import SessionLocal, LoanAssessment, init_db, get_db
from services.credit_limit import CreditLimitService
from features.feature_store import load_and_process

app = FastAPI(title="MSME Credit Risk MLOps API")

# Initialize DB
init_db()

# Globals to store models & services
MODELS = {}
LIMIT_SERVICE = None

@app.on_event("startup")
def load_models():
    """Load models and services on startup."""
    global LIMIT_SERVICE
    try:
        # Load from MLOps trained directory
        MODELS['classifier'] = joblib.load("models/trained/approval_model.pkl")
        MODELS['approval_cols'] = joblib.load("models/trained/approval_features.joblib")
        
        MODELS['pd_model'] = joblib.load("models/trained/pd_model.pkl")
        MODELS['pd_cols'] = joblib.load("models/trained/pd_features.joblib")
        
        # Initialize the decoupled service
        LIMIT_SERVICE = CreditLimitService("models/trained/credit_model.pkl")
        
        print("✅ Modular Models and Credit Service loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading MLOps models: {e}. Run mlops/pipeline.py first.")

class LoanRequest(BaseModel):
    business_id: str = "MSME_0001"
    age_years: int
    employees: int = 5
    annual_revenue: float
    net_profit: float
    total_assets: float
    fixed_assets: float
    valuation: float
    existing_debt: float
    cibil_score: int
    promoter_cibil: int
    udyam_registered: bool
    gst_compliant: bool
    requested_amount: float

@app.post("/predict")
def predict(request: LoanRequest, db: Session = Depends(get_db)):
    if not MODELS or not LIMIT_SERVICE:
        raise HTTPException(status_code=503, detail="Services not initialized")
    
    # 1. Hard Rejection Logic
    if not request.udyam_registered:
        res = create_rejection_response(request, "REJECTED: Udyam Registration is mandatory.")
        save_to_db(db, request, res)
        return res

    # 2. Process Features via Modular Pipeline
    input_dict = request.dict()
    # Add calculated fields for the pipeline
    input_dict['interest_expense'] = request.existing_debt * 0.12
    input_dict['principal_repayment'] = request.existing_debt * 0.10
    input_dict['ebitda'] = request.net_profit + input_dict['interest_expense'] + (request.total_assets * 0.05)
    input_dict['inventory_value'] = request.total_assets - request.fixed_assets
    
    input_df = pd.DataFrame([input_dict])
    features = load_and_process(input_df) # Uses modular build_features

    # 3. Approval & PD (Prob of Default)
    weighted_cibil = (request.cibil_score * 0.7 + request.promoter_cibil * 0.3)
    prob_paid = float(MODELS['classifier'].predict_proba(features[MODELS['approval_cols']])[0][1])
    prob_default = float(MODELS['pd_model'].predict_proba(features[MODELS['pd_cols']])[0][1])
    
    is_eligible = (
        request.gst_compliant and 
        weighted_cibil >= 650 and 
        prob_paid > 0.65
    )

    # 4. Limit Calculation via Decoupled Service
    limit_results = LIMIT_SERVICE.calculate_limit(features, input_dict)
    
    # 5. Ball Park Check
    is_in_ballpark = LIMIT_SERVICE.check_ballpark(request.requested_amount, limit_results['final_limit'])
    
    is_approved = is_eligible and is_in_ballpark
    
    # Final Remarks
    if not is_eligible:
        remarks = "REJECTED: Risk profile or compliance check failed."
    elif not is_in_ballpark:
        remarks = f"REJECTED: Outsized request. Maximum eligibility is ₹{limit_results['final_limit']:.1f}L."
    else:
        remarks = "APPROVED: Strong financial health and credit profile."

    result = {
        "approval_probability": prob_paid,
        "default_probability": prob_default,
        "is_approved": is_approved,
        "recommended_limit": limit_results['recommended_limit'],
        "max_allowable_loan": limit_results['max_loan_cap'],
        "final_loan_recommendation": limit_results['final_limit'],
        "remarks": remarks
    }
    
    # 6. Save to Database
    save_to_db(db, request, result)
    
    return result

def create_rejection_response(req, msg):
    return {
        "approval_probability": 0.0,
        "default_probability": 1.0,
        "is_approved": False,
        "recommended_limit": 0.0,
        "max_allowable_loan": 0.0,
        "final_loan_recommendation": 0.0,
        "remarks": msg
    }

def save_to_db(db: Session, req: LoanRequest, res: dict):
    try:
        db_record = LoanAssessment(
            business_id=req.business_id,
            is_approved=res['is_approved'],
            approval_probability=res['approval_probability'],
            final_limit=res['final_loan_recommendation'],
            remarks=res['remarks']
        )
        db.add(db_record)
        db.commit()
    except Exception as e:
        print(f"DB Save Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
