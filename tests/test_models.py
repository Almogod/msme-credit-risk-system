import pytest
import pandas as pd
import numpy as np
from features.build_features import build_features

def test_feature_engineering_ratios():
    """Test that financial ratios are calculated correctly and handle zero division."""
    data = {
        'annual_revenue': [100.0, 0.0],
        'net_profit': [10.0, -5.0],
        'total_assets': [500.0, 100.0],
        'existing_debt': [50.0, 0.0],
        'interest_expense': [5.0, 0.0],
        'principal_repayment': [5.0, 0.0],
        'ebitda': [20.0, 0.0],
        'fixed_assets': [300.0, 50.0]
    }
    df = pd.DataFrame(data)
    df_transformed = build_features(df)
    
    # Check DSCR for first row: 20 / (5 + 5) = 2.0
    assert df_transformed.loc[0, 'dscr'] == pytest.approx(2.0)
    
    # Check zero division handling for second row
    assert not np.isinf(df_transformed.loc[1, 'dscr']).any()
    assert df_transformed.loc[1, 'dscr'] == pytest.approx(0.0, abs=1e-5)

def test_clipping():
    """Test that financial columns are clipped to 0."""
    data = {'annual_revenue': [-100.0]}
    df = pd.DataFrame(data)
    df_transformed = build_features(df)
    assert df_transformed.loc[0, 'annual_revenue'] == 0.0
