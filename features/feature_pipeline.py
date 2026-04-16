import pandas as pd
import numpy as np

class FeaturePipeline:
    def __init__(self):
        self.feature_columns = [
            'age_years', 'annual_revenue', 'cibil_score', 'promoter_cibil',
            'udyam_registered', 'gst_compliant', 'total_assets', 'valuation',
            'dscr', 'icr', 'debt_to_equity', 'current_ratio', 'profit_margin'
        ]

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineers financial ratios localized for Indian banking standards.
        """
        df = df.copy()
        
        # 1. DSCR: EBITDA / (Principal + Interest)
        total_service = df['interest_expense'] + df['principal_repayment']
        df['dscr'] = df['ebitda'] / (total_service + 1e-6)
        
        # 2. ICR: EBITDA / Interest
        df['icr'] = df['ebitda'] / (df['interest_expense'] + 1e-6)
        
        # 3. Debt-to-Equity: existing_debt / shareholder_equity (simulated as assets - debt)
        equity = df['total_assets'] - df['existing_debt']
        df['debt_to_equity'] = df['existing_debt'] / (equity + 1e-6)
        
        # 4. Current Ratio: (Inventory + Cash) / (Current Debt approx)
        cash_proxy = df['annual_revenue'] * 0.15
        current_liabilities = df['existing_debt'] * 0.3 # assumption: 30% is current
        df['current_ratio'] = (df['inventory_value'] + cash_proxy) / (current_liabilities + 1e-6)

        # 5. Profit Margin
        df['profit_margin'] = df['net_profit'] / (df['annual_revenue'] + 1e-6)
        
        return df[self.feature_columns]

if __name__ == "__main__":
    # Test pipeline
    from services.data_loader import generate_msme_data
    
    print("Testing Feature Pipeline...")
    raw_df = generate_msme_data(5)
    pipeline = FeaturePipeline()
    features = pipeline.transform(raw_df)
    
    print("\nProcessed Features:")
    print(features.head())
    print("\nFeature Columns:", features.columns.tolist())
