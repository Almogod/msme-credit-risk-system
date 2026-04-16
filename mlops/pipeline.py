import os
import sys
import datetime

# Add project root to path
sys.path.append(os.getcwd())

from models.training import train_approval, train_credit, train_pd
from mlops.mlflow_tracking import get_tracker

def run_pipeline():
    print(f"[PROCESS] Starting MSME MLOps Pipeline - {datetime.datetime.now()}")
    
    tracker = get_tracker("MSME_Credit_Risk_v1")
    
    try:
        # 1. Training - Approval Model
        print("\n--- Phase 1: Approval Modeling ---")
        train_approval.train()
        tracker.log_metric("approval_trained", 1.0)
        
        # 2. Training - Credit Limit Model
        print("\n--- Phase 2: Credit Limit Modeling ---")
        train_credit.train()
        tracker.log_metric("credit_limit_trained", 1.0)
        
        # 3. Training - PD Model
        print("\n--- Phase 3: Probability of Default Modeling ---")
        train_pd.train()
        tracker.log_metric("pd_trained", 1.0)
        
        print("\nPipeline Execution Successful!")
        
    except Exception as e:
        print(f"\n❌ Pipeline Failed: {e}")
        tracker.log_metric("pipeline_success", 0.0)

if __name__ == "__main__":
    run_pipeline()
