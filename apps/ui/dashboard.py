import streamlit as st
import requests
import json
import pandas as pd

st.set_page_config(page_title="MSME Credit Risk Portal", layout="wide")

st.title("🏦 MSME Credit Risk Assessment Portal")
st.markdown("---")

# Sidebar for Business Details
st.sidebar.header("🏢 Business Profile")
age = st.sidebar.number_input("Years in Business", min_value=1, max_value=100, value=5)
employees = st.sidebar.number_input("Number of Employees", min_value=1, max_value=1000, value=20)
is_franchise = st.sidebar.selectbox("Franchise?", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
from services.database import SessionLocal, LoanAssessment
from sqlalchemy import desc

st.set_page_config(page_title="MSME Credit Risk Portal - India", layout="wide")

st.title("🏦 Enterprise MSME Credit Assessment")
st.write("Localized for Indian Banking Standards (RBI/MSME Guidelines)")

# Sidebar for analysis history
st.sidebar.header("📜 Recent Assessments")
db = SessionLocal()
history = db.query(LoanAssessment).order_by(desc(LoanAssessment.timestamp)).limit(5).all()
for h in history:
    status = "✅" if h.is_approved else "❌"
    st.sidebar.write(f"{status} {h.business_id} - ₹{h.final_limit:.1f}L")
db.close()

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
    debt = st.number_input("Existing Debt", value=5.0)
    requested = st.number_input("Loan Amount Requested", value=15.0)

    payload = {
        "business_id": b_id,
        "age_years": age,
        "annual_revenue": revenue,
        "net_profit": profit,
        "total_assets": assets,
        "existing_debt": debt,
        "cibil_score": cibil,
        "promoter_cibil": p_cibil,
        "udyam_registered": udyam,
        "gst_compliant": gst,
        "requested_amount": requested
    }
st.markdown("---")
st.caption("Enterprise MSME Credit Risk Analysis")
