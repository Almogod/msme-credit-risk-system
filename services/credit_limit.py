import joblib
import pandas as pd
import numpy as np

class CreditLimitService:
    def __init__(self, model_path: str = "models/trained/credit_model.pkl"):
        try:
            self.model = joblib.load(model_path)
            self.feature_cols = joblib.load("models/trained/credit_features.joblib")
        except:
            self.model = None
            self.feature_cols = []

    def calculate_limit(self, features_df: pd.DataFrame, financials: dict) -> dict:
        """
        Calculates the final credit limit using hybrid ML + Banking logic.
        """
        if self.model is None:
            return {"recommended_limit": 0, "max_loan_cap": 0, "final_limit": 0}

        # 1. ML-based Recommendation
        ml_limit = float(self.model.predict(features_df[self.feature_cols])[0])
        
        # 2. Asset-based Cap (50% LTV minus debt)
        total_assets = financials.get('total_assets', 0)
        existing_debt = financials.get('existing_debt', 0)
        max_loan_cap = max((total_assets * 0.5) - existing_debt, 0)
        
        # 3. Final Recommendation (The more conservative of the two)
        final_limit = min(ml_limit, max_loan_cap)
        
        return {
            "recommended_limit": round(ml_limit, 2),
            "max_loan_cap": round(max_loan_cap, 2),
            "final_limit": round(final_limit, 2)
        }

    def check_ballpark(self, requested: float, final_limit: float) -> bool:
        """Checks if requested amount is within 10% of eligibility."""
        return requested <= (final_limit * 1.1)
