import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())
from features.feature_store import load_and_process

def train():
    print("🚀 Training Approval Model...")
    
    # Check for raw data
    data_path = "data/raw/msme_loans.csv"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Generate data first.")
        return

    # Load and process features
    df = load_and_process(data_path)
    
    # Target: approved
    target = "approved"
    
    # Feature Selection for Approval
    # Excluding non-feature or future-revealing columns
    exclude = [target, 'business_id', 'mis_status', 'requested_amount']
    X = df.drop(columns=[c for c in exclude if c in df.columns])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Configure robust classifier
    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        use_label_encoder=False,
        eval_metric='logloss'
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"✅ Approval Model Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, preds))

    # Save model
    os.makedirs("models/trained", exist_ok=True)
    joblib.dump(model, "models/trained/approval_model.pkl")
    # Save the feature list for inference consistency
    joblib.dump(X.columns.tolist(), "models/trained/approval_features.joblib")
    
    print(f"Model saved to models/trained/approval_model.pkl")

if __name__ == "__main__":
    train()
