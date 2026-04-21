import pandas as pd
import numpy as np
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, ClassificationPreset
import os

class DriftMonitor:
    """
    Service to monitor data and model drift using Evidently.
    """
    def __init__(self, report_dir: str = "reports/drift"):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)

    def generate_drift_report(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, filename: str = "data_drift.html"):
        """
        Generates a comprehensive data drift report.
        """
        report = Report(metrics=[
            DataDriftPreset(),
            TargetDriftPreset(),
        ])
        
        report.run(reference_data=reference_data, current_data=current_data)
        report_path = os.path.join(self.report_dir, filename)
        report.save_html(report_path)
        print(f"✅ Drift report saved to {report_path}")
        return report_path

    def generate_performance_report(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, target_col: str, filename: str = "model_performance.html"):
        """
        Generates a model performance report comparing reference vs current batches.
        """
        report = Report(metrics=[
            ClassificationPreset(),
        ])
        
        report.run(reference_data=reference_data, current_data=current_data)
        report_path = os.path.join(self.report_dir, filename)
        report.save_html(report_path)
        print(f"✅ Performance report saved to {report_path}")
        return report_path

if __name__ == "__main__":
    # Example usage / smoke test with synthetic data
    monitor = DriftMonitor()
    ref = pd.DataFrame(np.random.randn(100, 5), columns=['f1', 'f2', 'f3', 'f4', 'f5'])
    curr = pd.DataFrame(np.random.randn(100, 5) + 0.1, columns=['f1', 'f2', 'f3', 'f4', 'f5'])
    monitor.generate_drift_report(ref, curr)
