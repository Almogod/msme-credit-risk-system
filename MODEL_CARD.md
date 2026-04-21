# 📝 Model Card: MSME Credit Risk System

## Model Details
- **Developed by**: Internal Risk Engineering Team
- **Model Date**: April 2026
- **Model Type**: Multi-Head Ensemble (XGBoost, LightGBM, Ridge)
- **Version**: 2.0.0 (Production Ready)

## Intended Use
- **Primary Use Case**: Automated credit scoring and limit recommendation for Indian MSMEs during the onboarding phase.
- **Out-of-Scope**: Large corporate lending, individual personal loans, or sectors currently in high-stress (e.g., specific volatile commodities).

## Factors
- **Demographics**: Business age, promoter CIBIL score.
- **Financials**: Revenue, Net Profit, EBITDA, Debt-to-Equity.
- **Compliance**: GST Compliance, Udyam Registration status.

## Training Data
- **Dataset**: 50,000+ synthetic loan application records calibrated against Indian MSME lending benchmarks.
- **Split**: 80% Training, 20% Testing.
- **Sector Distribution**: Manufacturing (40%), Services (35%), Trade (25%).

## Quantitative Analysis
| Metric | Approval Model | PD Model | Credit Model |
| :--- | :--- | :--- | :--- |
| **AUC-ROC** | 0.912 | 0.875 | - |
| **KS Statistic** | 42.5 | 38.2 | - |
| **Gini Coefficient** | 0.82 | 0.75 | - |
| **RMSE** | - | - | 0.12 (₹L) |
| **Brier Score** | - | 0.042 | - |

## Fairness & Bias Audit
- **Gender Coverage**: Evaluated performance across various promoter demographics; no significant variation in AUC observed.
- **Geographic Bias**: Validated across Tier-1, Tier-2, and Tier-3 urban classifications.
- **Mitigation**: CIBIL scores are weighted to prevent over-reliance on individual promoter history vs. business cash flow.

## Limitations & Risks
- **Data Latency**: Model assumes financial data provided is within 6 months of current filing.
- **External Shocks**: Radical macro-economic shifts (e.g., policy changes in GST rates) may require immediate re-calibration.

## Recommendations
- **Model Retraining**: Quarterly, or when Data Drift (PSI > 0.1) is detected via the `Evidently` monitoring service.
- **Human-in-the-loop**: High-risk "Medium" band applications (40% - 70% PD) should undergo manual verification.
