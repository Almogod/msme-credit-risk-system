import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())
from features.feature_store import load_and_process

def train():
    print("[TRAIN] Training Credit Limit Model...")
    
    data_path = "data/raw/msme_loans.csv"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Generate data first.")
        return

    df = load_and_process(data_path)
    
    # Target: requested_amount (as proxy for sanctioned limit in synthetic data)
    target = "requested_amount"
    
    # Feature Selection
    exclude = [target, 'business_id', 'mis_status', 'approved']
    X = df.drop(columns=[c for c in exclude if c in df.columns])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Configure regressor
    model = XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        objective='reg:squarederror'
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print(f"[METRIC] Credit Model MAE: {mae:.2f}")
    print(f"[METRIC] Credit Model R2: {r2:.4f}")

    # Save model
    os.makedirs("models/trained", exist_ok=True)
    joblib.dump(model, "models/trained/credit_model.pkl")
    joblib.dump(X.columns.tolist(), "models/trained/credit_features.joblib")
    
    print(f"Model saved to models/trained/credit_model.pkl")

if __name__ == "__main__":
    train()
