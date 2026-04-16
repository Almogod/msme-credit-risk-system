import streamlit as st
import requests
import pandas as pd
from services.database import SessionLocal, LoanAssessment
from sqlalchemy import desc

st.set_page_config(page_title="MSME Credit Risk Portal - India", layout="wide")

st.title("🏦 Enterprise MSME Credit Assessment")
st.write("Localized for Indian Banking Standards (RBI/MSME Guidelines)")

# Sidebar for analysis history
st.sidebar.header("📜 Recent Assessments")
try:
    db = SessionLocal()
    history = db.query(LoanAssessment).order_by(desc(LoanAssessment.timestamp)).limit(5).all()
    for h in history:
        status = "✅" if h.is_approved else "❌"
        st.sidebar.write(f"{status} {h.business_id} - ₹{h.final_limit:.1f}L")
    db.close()
except Exception as e:
    st.sidebar.error("Database connection failed. Ensure the server is initialized.")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Business Profile")
    b_id = st.text_input("Business ID", value="MSME_001")
    age = st.number_input("Business Vintage (Years)", min_value=1, max_value=50, value=3)
    
    st.divider()
    st.subheader("Compliance Check")
    udyam = st.checkbox("Udyam Registered?", value=True)
    gst = st.checkbox("GST Compliant?", value=True)
    
    st.divider()
    st.subheader("Credit Health")
    cibil = st.slider("Business CIBIL Rank", 300, 900, 750)
    p_cibil = st.slider("Promoter Personal CIBIL", 300, 900, 720)
    
    st.divider()
    st.subheader("Financials (₹ Lakhs)")
    revenue = st.number_input("Annual Turnover", value=50.0)
    profit = st.number_input("Net Profit", value=8.5)
    assets = st.number_input("Total Fixed Assets", value=30.0)
    valuation = st.number_input("Current Valuation", value=60.0)
    debt = st.number_input("Existing Debt", value=5.0)
    requested = st.number_input("Loan Amount Requested", value=15.0)

    payload = {
        "business_id": b_id,
        "age_years": age,
        "annual_revenue": revenue,
        "net_profit": profit,
        "total_assets": assets,
        "valuation": valuation,
        "existing_debt": debt,
        "cibil_score": cibil,
        "promoter_cibil": p_cibil,
        "udyam_registered": udyam,
        "gst_compliant": gst,
        "requested_amount": requested
    }

    if st.button("🚀 Run Risk Assessment"):
        try:
            response = requests.post("http://localhost:8000/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                
                with col2:
                    st.subheader("Decision Results")
                    
                    if result['is_approved']:
                        st.success(f"✅ **STATUS: {result['remarks']}**")
                    else:
                        st.error(f"❌ **STATUS: {result['remarks']}**")
                    
                    # Metrics
                    m1, m2 = st.columns(2)
                    m1.metric("Approval Prob.", f"{result['approval_probability']*100:.1f}%")
                    m2.metric("Final Limit", f"₹{result['final_loan_recommendation']:.2f} L")
                    
                    if result['feature_importance']:
                        st.divider()
                        st.subheader("🔍 Explainability (SHAP)")
                        fi = result['feature_importance']
                        fi_df = pd.DataFrame(list(fi.items()), columns=['Feature', 'SHAP Value'])
                        fi_df = fi_df.sort_values(by='SHAP Value', key=abs, ascending=False).head(8)
                        st.bar_chart(fi_df, x='Feature', y='SHAP Value')
                        st.caption("Positive values increase approval chance, negative decrease it.")

                    st.divider()
                    st.write("**Financial Summary:**")
                    st.write(f"- ML Limit: ₹{result['recommended_limit']:.2f} L")
                    st.write(f"- Asset Cap: ₹{result['max_allowable_loan']:.2f} L")
            else:
                st.error(f"API Error: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to Prediction API. Make sure the backend is running. Error: {e}")

st.markdown("---")
st.caption("Enterprise MSME Credit Risk Analysis - Powered by SHAP & XGBoost")
