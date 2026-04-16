import pandas as pd
import numpy as np
from faker import Faker
import os

fake = Faker()
np.random.seed(42)

def generate_msme_data(n_samples=1000):
    """
    Generates synthetic Indian MSME data including CIBIL, GST, and Udyam metrics.
    """
    data = []
    
    for i in range(n_samples):
        # Business metadata
        business_age = np.random.randint(1, 30)
        employees = np.random.randint(1, 250)
        is_franchise = np.random.choice([0, 1], p=[0.95, 0.05])
        
        # Operational Metrics (In INR Lakhs)
        # turnover ₹10L to ₹10Cr
        annual_revenue = np.random.uniform(10, 1000) 
        net_profit_margin = np.random.uniform(0.02, 0.20)
        annual_net_profit = annual_revenue * net_profit_margin
        
        # Qualitative & Compliance (Critical for India)
        udyam_registered = np.random.choice([0, 1], p=[0.2, 0.8])
        gst_compliant = np.random.choice([0, 1], p=[0.1, 0.9])
        cibil_score = np.random.randint(300, 900)
        promoter_cibil = np.random.randint(600, 850)
        
        # Assets & Liabilities
        fixed_assets = annual_revenue * np.random.uniform(0.3, 1.2) # Slightly wider range
        inventory_value = annual_revenue * np.random.uniform(0.1, 0.4)
        total_assets = fixed_assets + inventory_value + (annual_revenue * 0.2)
        
        valuation = total_assets * np.random.uniform(1.5, 3.0) 
        existing_debt = total_assets * np.random.uniform(0.1, 0.4)
        
        # Debt Service Components (Calibrated with Kaggle Patterns)
        # 1. Interest Rate: 8% to 22% (Kaggle range)
        # 2. Tenure: 12 to 84 months
        interest_rate = np.random.uniform(0.08, 0.22)
        tenure_months = np.random.choice([12, 24, 36, 48, 60, 72, 84])
        
        interest_expense = (existing_debt * interest_rate)
        principal_repayment = (existing_debt / (tenure_months / 12)) if exists_debt else 0
        
        total_debt_service = interest_expense + principal_repayment
        
        # Loan Request (Calibrated: Matches Kaggle's DTI and Amount distributions)
        # Generally 2x to 5x of annual profit
        requested_amount = (annual_net_profit * np.random.uniform(2, 5)) + (total_assets * 0.1)
        requested_amount = max(requested_amount, 5) 
        
        # Target: Approval (Kaggle-Infused logic)
        ebitda = annual_net_profit + interest_expense + (total_assets * 0.05)
        dscr = ebitda / (total_debt_service + 1e-6)
        
        # Calibration weights
        # Higher interest (Kaggle pattern) = Higher default risk
        interest_risk = (interest_rate - 0.08) / 0.14 
        
        if udyam_registered == 0 or cibil_score < 600 or gst_compliant == 0:
            approved = 0
            mis_status = 0
        else:
            cibil_norm = (cibil_score - 300) / 600
            score = (
                (cibil_norm * 0.40) + 
                (min(dscr/2.0, 1.0) * 0.30) + 
                (gst_compliant * 0.15) + 
                (net_profit_margin * 5 * 0.15)
            )
            
            approval_prob = 1 / (1 + np.exp(-(score - 0.55) * 10))
            approved = 1 if np.random.random() < approval_prob else 0
            
            # Default risk increases with high interest rates and low DSCR
            default_risk = 1 / (1 + np.exp((score - 0.35 - (interest_risk * 0.2)) * 8))
            mis_status = 1 if np.random.random() > default_risk else 0
            
        data.append({
            "business_id": f"MSME_{i:04d}",
            "age_years": business_age,
            "annual_revenue": annual_revenue,
            "net_profit": annual_net_profit,
            "ebitda": ebitda,
            "cibil_score": cibil_score,
            "promoter_cibil": promoter_cibil,
            "udyam_registered": udyam_registered,
            "gst_compliant": gst_compliant,
            "fixed_assets": fixed_assets,
            "inventory_value": inventory_value,
            "total_assets": total_assets,
            "valuation": valuation,
            "existing_debt": existing_debt,
            "interest_expense": interest_expense,
            "principal_repayment": principal_repayment,
            "requested_amount": requested_amount,
            "approved": approved,
            "mis_status": mis_status 
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating synthetic MSME dataset...")
    df = generate_msme_data(2000)
    
    # Create directories if they don't exist
    os.makedirs("data/raw", exist_ok=True)
    
    save_path = "data/raw/msme_loans.csv"
    df.to_csv(save_path, index=False)
    print(f"Dataset saved to {save_path} ({len(df)} records)")
    
    # Basic Summary
    print("\nDataset Preview:")
    print(df.head())
    print("\nApproval Rate:", df['approved'].mean())
    print("Default Rate (of approved):", 1 - df[df['approved']==1]['mis_status'].mean())
