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

from services.database import SessionLocal, LoanAssessment, init_db
from sqlalchemy.orm import Session
from fastapi import Depends

init_db() # Run migrations

class LoanRequest(BaseModel):
    business_id: str = "MSME_0001"
    age_years: int
    annual_revenue: float # In Lakhs
    net_profit: float
    total_assets: float
    existing_debt: float
    cibil_score: int
    promoter_cibil: int
    udyam_registered: bool
    gst_compliant: bool
    requested_amount: float

@app.post("/predict")
def predict(request: LoanRequest, db: Session = Depends(SessionLocal)):
    if not MODELS:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    # 1. Hard Rejection Logic (User requirement)
    if not request.udyam_registered:
        res = {
            "approval_probability": 0.0,
            "is_approved": False,
            "recommended_limit": 0.0,
            "max_allowable_loan": 0.0,
            "final_loan_recommendation": 0.0,
            "feature_importance": {},
            "remarks": "REJECTED: Udyam Registration is a mandatory requirement for this loan scheme."
        }
        # Save to DB even for rejections
        save_to_db(db, request, res)
        return res

    # 2. Prepare Data for Model
    input_dict = request.dict()
    # Simulate internal calculations needed for pipeline
    input_dict['interest_expense'] = request.existing_debt * 0.12 # assume 12% avg
    input_dict['principal_repayment'] = request.existing_debt * 0.10
    input_dict['ebitda'] = request.net_profit + input_dict['interest_expense'] + (request.total_assets * 0.05)
    input_dict['inventory_value'] = request.total_assets * 0.2
    
    input_df = pd.DataFrame([input_dict])
    
    # Transform
    features = MODELS['pipeline'].transform(input_df)
    
    # Approval Prediction
    # Weighted CIBIL score internal logic (from user requirement)
    weighted_cibil = (request.cibil_score * 0.6 + request.promoter_cibil * 0.4)
    prob_paid = float(MODELS['classifier'].predict_proba(features)[0][1])
    
    # Final approval depends on both ML and hard thresholds
    is_approved = prob_paid > 0.6 and weighted_cibil > 650
    
    # SHAP Explainability
    shap_vals = MODELS['explainer'].shap_values(features)
    feature_importance = dict(zip(features.columns, shap_vals[0].tolist()))
    
    # Limit Prediction
    recommended_limit = float(MODELS['regressor'].predict(features)[0])
    
    # Asset-based max loan (Valuation Logic)
    max_loan_cap = request.total_assets * 0.5 - request.existing_debt
    max_loan_cap = max(max_loan_cap, 0)
    
    # Final Recommendation
    final_limit = min(recommended_limit, max_loan_cap)
    
    result = {
        "approval_probability": prob_paid,
        "is_approved": is_approved,
        "recommended_limit": recommended_limit,
        "max_allowable_loan": max_loan_cap,
        "final_loan_recommendation": final_limit if is_approved else 0,
        "feature_importance": feature_importance,
        "remarks": "Loan approved based on cash flow and credit health." if is_approved else "Loan rejected due to risk profiles."
    }
    
    # 3. Save to Database
    save_to_db(db, request, result)
    
    return result

def save_to_db(db: Session, req: LoanRequest, res: dict):
    try:
        db_record = LoanAssessment(
            business_id=req.business_id,
            age_years=req.age_years,
            annual_revenue=req.annual_revenue,
            net_profit=req.net_profit,
            total_assets=req.total_assets,
            total_debt=req.existing_debt,
            cibil_score=req.cibil_score,
            udyam_registered=req.udyam_registered,
            gst_compliant=req.gst_compliant,
            is_approved=res['is_approved'],
            approval_probability=res['approval_probability'],
            recommended_limit=res['recommended_limit'],
            max_loan_cap=res['max_loan_cap'],
            final_limit=res['final_loan_recommendation'],
            feature_importance=res['feature_importance'],
            remarks=res['remarks']
        )
        db.add(db_record)
        db.commit()
    except Exception as e:
        print(f"Database Save Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
