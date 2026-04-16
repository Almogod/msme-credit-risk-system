import pandas as pd
import numpy as np

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers financial ratios for Indian MSMEs with edge-case robustness.
    Includes: DSCR, ICR, Debt-to-Equity, and Current Ratio.
    """
    df = df.copy()

    # 1. Protection against Zero/Negative Financials
    # In banking, negative revenue/assets are data entry errors or extreme distress
    cols_to_clip = ['annual_revenue', 'total_assets', 'ebitda', 'net_profit']
    for col in cols_to_clip:
        if col in df.columns:
            df[col] = df[col].clip(lower=0)

    # 2. DSCR: EBITDA / (Principal + Interest)
    # Edge case: Zero debt service (no existing debt)
    if 'interest_expense' in df.columns and 'principal_repayment' in df.columns:
        total_service = df['interest_expense'] + df['principal_repayment']
        df['dscr'] = df['ebitda'] / (total_service + 1e-6)
    else:
        df['dscr'] = 2.0 # Assume healthy if no debt info available

    # 3. ICR: EBITDA / Interest
    if 'interest_expense' in df.columns:
        df['icr'] = df['ebitda'] / (df['interest_expense'] + 1e-6)
    else:
        df['icr'] = 5.0 # Assume healthy

    # 4. Debt-to-Equity
    if 'total_assets' in df.columns and 'existing_debt' in df.columns:
        equity = df['total_assets'] - df['existing_debt']
        df['debt_to_equity'] = df['existing_debt'] / (equity.clip(lower=1) + 1e-6)
    else:
        df['debt_to_equity'] = 0.5

    # 5. Current Ratio
    if 'inventory_value' in df.columns and 'annual_revenue' in df.columns:
        cash_proxy = df['annual_revenue'] * 0.15
        current_liabilities = df.get('existing_debt', 0) * 0.3
        df['current_ratio'] = (df['inventory_value'] + cash_proxy) / (current_liabilities + 1e-6)
    else:
        df['current_ratio'] = 1.5

    # 6. Profit Margin
    if 'net_profit' in df.columns and 'annual_revenue' in df.columns:
        df['profit_margin'] = df['net_profit'] / (df['annual_revenue'] + 1e-6)

    # Handle NaNs created by edge cases
    df = df.fillna(0)

    return df
