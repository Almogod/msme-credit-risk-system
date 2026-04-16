import pandas as pd
import numpy as np

class FeaturePipeline:
    def __init__(self):
        self.feature_columns = [
            'age_years', 'employees', 'is_franchise', 'urban_rural',
            'fixed_assets', 'inventory_value', 'total_assets', 'valuation',
            'existing_debt', 'requested_amount',
            'debt_to_asset_ratio', 'profit_margin', 'asset_utilization',
            'liquidity_ratio'
        ]

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineers financial ratios and cleans data.
        """
        df = df.copy()
        
        # 1. Debt-to-Asset Ratio
        df['debt_to_asset_ratio'] = df['existing_debt'] / (df['total_assets'] + 1e-6)
        
        # 2. Profit Margin
        df['profit_margin'] = df['net_profit'] / (df['annual_revenue'] + 1e-6)
        
        # 3. Asset Utilization (Revenue per unit of asset)
        df['asset_utilization'] = df['annual_revenue'] / (df['total_assets'] + 1e-6)
        
        # 4. Liquidity Ratio (Proxy: Inventory + Cash (10% rev) / Requested + existing debt)
        cash_proxy = df['annual_revenue'] * 0.1
        df['liquidity_ratio'] = (df['inventory_value'] + cash_proxy) / (df['existing_debt'] + df['requested_amount'] + 1e-6)
        
        # Log Transforms for skewed financial data
        financial_cols = ['fixed_assets', 'inventory_value', 'total_assets', 'valuation', 'annual_revenue', 'net_profit']
        for col in financial_cols:
            df[f'log_{col}'] = np.log1p(df[col].clip(lower=0))
            
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
