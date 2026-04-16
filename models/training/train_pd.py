import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, brier_score_loss
from xgboost import XGBClassifier
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())
from features.feature_store import load_and_process

def train():
    print("[TRAIN] Training Probability of Default (PD) Model...")
    
    data_path = "data/raw/msme_loans.csv"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    df = load_and_process(data_path)
    
    # Target: mis_status (1 if defaulted/default probability, 0 otherwise)
    # Note: In our synthetic data, mis_status=1 is a 'problematic' case.
    target = "mis_status"
    
    exclude = [target, 'business_id', 'approved', 'requested_amount']
    X = df.drop(columns=[c for c in exclude if c in df.columns])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # PD Model needs well-calibrated probabilities
    model = XGBClassifier(
        n_estimators=150,
        max_depth=4,
        learning_rate=0.01,
        objective='binary:logistic'
    )

    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probs)
    brier = brier_score_loss(y_test, probs)

    print(f"[METRIC] PD Model AUC: {auc:.4f}")
    print(f"[METRIC] Brier Score (Calibration): {brier:.4f}")

    # Save model
    os.makedirs("models/trained", exist_ok=True)
    joblib.dump(model, "models/trained/pd_model.pkl")
    joblib.dump(X.columns.tolist(), "models/trained/pd_features.joblib")
    
    print(f"Model saved to models/trained/pd_model.pkl")

if __name__ == "__main__":
    train()
