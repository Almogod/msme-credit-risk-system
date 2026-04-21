import mlflow
import os

class MLFlowTracker:
    """
    A production-grade wrapper for MLflow tracking.
    """
    def __init__(self, experiment_name: str):
        self.tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name
        self.active_run = None

    def start_run(self, run_name: str = None):
        self.active_run = mlflow.start_run(run_name=run_name)
        return self.active_run

    def end_run(self):
        if self.active_run:
            mlflow.end_run()
            self.active_run = None

    def log_param(self, key: str, value):
        mlflow.log_param(key, value)

    def log_metric(self, key: str, value):
        mlflow.log_metric(key, value)

    def log_model(self, model, artifact_path: str):
        mlflow.sklearn.log_model(model, artifact_path)

    def log_artifact(self, local_path: str):
        mlflow.log_artifact(local_path)

def get_tracker(experiment: str):
    return MLFlowTracker(experiment)
