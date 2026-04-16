import pandas as pd
import numpy as np
from faker import Faker
import os

fake = Faker()
np.random.seed(42)

def generate_msme_data(n_samples=1000):
    """
    Generates synthetic MSME data matching SBA patterns plus additional asset/valuation metrics.
    """
    data = []
    
    for i in range(n_samples):
        # Business metadata
        business_age = np.random.randint(1, 30)
        employees = np.random.randint(1, 250)
        is_franchise = np.random.choice([0, 1], p=[0.9, 0.1])
        urban_rural = np.random.choice([1, 2, 0]) # 1=Urban, 2=Rural, 0=Undefined
        
        # Financials (scaled by size and age)
        annual_revenue = employees * np.random.uniform(50000, 200000) * (1 + (business_age/30))
        net_profit_margin = np.random.uniform(-0.05, 0.25)
        annual_net_profit = annual_revenue * net_profit_margin
        
        # Assets & Valuation (The "Enterprise" features requested)
        fixed_assets = annual_revenue * np.random.uniform(0.1, 0.5)
        inventory_value = annual_revenue * np.random.uniform(0.05, 0.2)
        total_assets = fixed_assets + inventory_value + (annual_revenue * 0.1) # plus cash
        
        valuation = total_assets * np.random.uniform(0.8, 1.5) # Based on asset + income multiplier
        
        existing_debt = total_assets * np.random.uniform(0, 0.6)
        
        # Loan Request
        requested_amount = annual_revenue * np.random.uniform(0.1, 0.4)
        
        # Target: Approval (Simplified logic for synthetic data generation)
        # Approval depends on Debt-to-Revenue, Age, and Profitability
        dti = existing_debt / annual_revenue
        score = (business_age / 30) * 0.3 + (net_profit_margin * 2) + (1 - dti) * 0.4
        approval_prob = 1 / (1 + np.exp(-score))
        approved = 1 if np.random.random() < approval_prob else 0
        
        # Actual status (Default probability)
        # Higher score = Lower chance of default
        default_prob = 1 / (1 + np.exp(score - 1))
        mis_status = 1 if np.random.random() > default_prob else 0 # 1=Paid, 0=Defaulted
        
        data.append({
            "business_id": f"MSME_{i:04d}",
            "age_years": business_age,
            "employees": employees,
            "is_franchise": is_franchise,
            "urban_rural": urban_rural,
            "annual_revenue": annual_revenue,
            "net_profit": annual_net_profit,
            "fixed_assets": fixed_assets,
            "inventory_value": inventory_value,
            "total_assets": total_assets,
            "valuation": valuation,
            "existing_debt": existing_debt,
            "requested_amount": requested_amount,
            "approved": approved,
            "mis_status": mis_status # Target for Loan Approval Model
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
