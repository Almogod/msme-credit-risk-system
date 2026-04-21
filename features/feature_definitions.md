# 📊 Feature Definitions & Credit Underwriting Logic

This document defines the features used in the MSME Credit Risk System and explains their significance in the credit underwriting process.

## Financial Ratios (Engineered)

### 1. DSCR (Debt Service Coverage Ratio)
- **Formula**: `EBITDA / (Principal Repayment + Interest Expense + 1e-6)`
- **Interpretation**: Measures the business's ability to use its operating income to repay all its debt obligations. 
- **Underwriting Benchmark**: `> 1.25` is generally considered healthy. `< 1.0` indicates insufficient cash flow to service debt.

### 2. ICR (Interest Coverage Ratio)
- **Formula**: `EBITDA / (Interest Expense + 1e-6)`
- **Interpretation**: Specifically focuses on the ability to pay interest on outstanding debt.
- **Underwriting Benchmark**: Higher is better. A ratio of `2.0` is typically the minimum threshold for comfort.

### 3. Current Ratio
- **Formula**: `(Inventory Value + Cash Proxy) / (Current Liabilities + 1e-6)`
- **Interpretation**: Measures short-term liquidity — the ability to pay off obligations due within one year.
- **Underwriting Benchmark**: `> 1.5` indicates strong liquidity.

### 4. Debt-to-Equity Ratio
- **Formula**: `Existing Debt / (Equity + 1e-6)`
- **Interpretation**: Indicates the relative proportion of shareholders' equity and debt used to finance a company's assets.
- **Underwriting Benchmark**: `< 2.0` is standard for MSMEs. High leverage increases risk of insolvency.

### 5. Profit Margin
- **Formula**: `Net Profit / (Annual Revenue + 1e-6)`
- **Interpretation**: Measures how much out of every rupee of sales a company actually keeps in earnings.

---

## Credit & Compliance Features

| Feature Name | Description | Underwriting Significance |
| :--- | :--- | :--- |
| **CIBIL Score** | Bureau credit score of the business. | Core indicator of repayment history and creditworthiness. |
| **Promoter CIBIL** | Personal credit score of the business owner. | High correlation with MSME repayment, especially for proprietorships. |
| **GST Compliant** | Boolean flag for active & clean GST filings. | Proxy for business legitimacy and "white" revenue records. |
| **Udyam Registered** | Registration with Ministry of MSME. | Mandatory for priority sector lending (PSL) benefits. |
| **Age Years** | Number of years since incorporation. | Older businesses generally exhibit more stability and lower default risk. |

---

## Decline Reason Mapping
The system identifies the following "Top Decline Reasons" based on feature thresholds:
- **Low DSCR**: Insufficient cash flow to service requested debt.
- **High Leverage**: Debt-to-Equity ratio exceeds risk appetite.
- **Bureau Fragility**: CIBIL or Promoter CIBIL scores fall below the 650 threshold.
- **Compliance Failure**: Lack of GST compliance or Udyam registration.
