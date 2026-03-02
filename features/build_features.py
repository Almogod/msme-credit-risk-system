import pandas as pd

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Example feature engineering
    df["debt_to_income"] = df["loan_amount"] / (df["income"] + 1)
    df["credit_utilization"] = df["loan_amount"] / (df["assets"] + 1)

    df["income_to_loan_ratio"] = df["income"] / (df["loan_amount"] + 1)

    # Drop unnecessary columns
    df = df.fillna(0)

    return df
