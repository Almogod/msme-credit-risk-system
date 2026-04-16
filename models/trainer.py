import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
import joblib
import os
import sys
import shap

# Add project root to path for local imports
sys.path.append(os.getcwd())

from features.feature_pipeline import FeaturePipeline

def train_models():
    """
    Trains the Loan Approval Classifier and Credit Limit Regressor, including SHAP.
    """
    if not os.path.exists("data/raw/msme_loans.csv"):
        print("Data not found. Run services/data_loader.py first.")
        return

    # 1. Load Data
    print("Loading data...")
    df = pd.read_csv("data/raw/msme_loans.csv")
    
    # 2. Preprocess
    print("Preprocessing data...")
    pipeline = FeaturePipeline()
    X = pipeline.transform(df)
    
    # Targets
    y_class = df['mis_status'] # 1=Paid, 0=Default
    y_reg = df['requested_amount'] # Amount granted/limit
    
    # Split
    X_train, X_test, y_class_train, y_class_test = train_test_split(X, y_class, test_size=0.2, random_state=42)
    _, _, y_reg_train, y_reg_test = train_test_split(X, y_reg, test_size=0.2, random_state=42)
    
    # 3. Train Loan Approval Model (XGBoost)
    print("Training Loan Approval Model...")
    clf = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    clf.fit(X_train, y_class_train)
    
    # 4. Generate SHAP Explainer
    print("Generating SHAP Explainer...")
    explainer = shap.TreeExplainer(clf)
    
    # Eval
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_class_test, y_pred)
    print(f"Approval Model Accuracy: {acc:.4f}")
    
    # 5. Train Credit Limit Model (Random Forest)
    print("Training Credit Limit Model...")
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X_train, y_reg_train)
    
    # Eval
    y_reg_pred = reg.predict(X_test)
    mae = mean_absolute_error(y_reg_test, y_reg_pred)
    r2 = r2_score(y_reg_test, y_reg_pred)
    print(f"Credit Limit Model - MAE: {mae:.2f}, R2: {r2:.4f}")
    
    # 6. Save Models & Explainer
    os.makedirs("models/saved", exist_ok=True)
    joblib.dump(clf, "models/saved/classifier.joblib")
    joblib.dump(reg, "models/saved/regressor.joblib")
    joblib.dump(pipeline, "models/saved/pipeline.joblib")
    joblib.dump(explainer, "models/saved/explainer.joblib")
    
    print("\nModels, pipeline, and SHAP explainer saved to models/saved/")

if __name__ == "__main__":
    train_models()

if __name__ == "__main__":
    train_models()
