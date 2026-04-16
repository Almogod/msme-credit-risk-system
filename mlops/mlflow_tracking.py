import os

class MLFlowTracker:
    """
    A lightweight wrapper for ML metadata tracking.
    Can be expanded to use the actual mlflow library.
    """
    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        self.active_run = None
        print(f"[TRACKER] MLflow Tracker initialized: Experiment '{experiment_name}'")

    def log_param(self, key: str, value):
        print(f"   [PARAM] {key}: {value}")

    def log_metric(self, key: str, value):
        print(f"   [METRIC] {key}: {value:.4f}")

    def log_model(self, model, artifact_path: str):
        print(f"   [MODEL] Artifact saved at: {artifact_path}")

def get_tracker(experiment: str):
    return MLFlowTracker(experiment)
