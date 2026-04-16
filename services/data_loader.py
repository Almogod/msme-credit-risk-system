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
        fixed_assets = annual_revenue * np.random.uniform(0.2, 0.8)
        inventory_value = annual_revenue * np.random.uniform(0.1, 0.3)
        total_assets = fixed_assets + inventory_value + (annual_revenue * 0.15)
        
        valuation = total_assets * np.random.uniform(1.2, 2.5) 
        existing_debt = total_assets * np.random.uniform(0.1, 0.5)
        
        # Debt Service Components (for DSCR/ICR)
        interest_rate = np.random.uniform(0.08, 0.18)
        interest_expense = existing_debt * interest_rate
        principal_repayment = existing_debt * 0.1 # assuming 10% principal annually
        
        total_debt_service = interest_expense + principal_repayment
        
        # Loan Request
        requested_amount = annual_revenue * np.random.uniform(0.2, 0.5)
        
        # Target: Approval (Common Sense calibrated logic for India)
        # 1. CIBIL Impact (45%)
        # 2. DSCR Impact (25%) - High penalty for < 1.0
        # 3. GST Compliance (15%)
        # 4. Business Vintage (10%)
        # 5. Profitability (5%)
        
        # Hard rejection logic (Common Sense Gatekeepers)
        if udyam_registered == 0 or cibil_score < 600 or gst_compliant == 0:
            approved = 0
            mis_status = 0
        else:
            # Calibrated weights
            cibil_norm = (cibil_score - 300) / 600
            dscr_impact = min(dscr / 2.0, 1.2) # cap impact, but rewarding for > 1.25
            age_impact = min(business_age / 10, 1.0) # stability reached at 10 years
            
            score = (
                (cibil_norm * 0.45) + 
                (dscr_impact * 0.25) + 
                (gst_compliant * 0.15) + 
                (age_impact * 0.10) + 
                (net_profit_margin * 5 * 0.05) # Scaling 20% margin to 1.0
            )
            
            # Sigmoid for probabilistic approval around the 0.6 threshold
            approval_prob = 1 / (1 + np.exp(-(score - 0.6) * 12))
            approved = 1 if np.random.random() < approval_prob else 0
            
            # Default logic: Highly tied to lack of DSCR and over-leverage
            default_risk = 1 / (1 + np.exp((score - 0.4) * 8))
            mis_status = 1 if np.random.random() > default_risk else 0
            
        data.append({
            "business_id": f"MSME_{i:04d}",
            "age_years": business_age,
            "employees": employees,
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
