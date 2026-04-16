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
urban_rural = st.sidebar.selectbox("Location Type", [1, 2, 0], format_func=lambda x: {1: "Urban", 2: "Rural", 0: "Other"}[x])

st.sidebar.header("📊 Financial Metrics")
revenue = st.sidebar.number_input("Annual Revenue ($)", min_value=0.0, value=500000.0, step=10000.0)
profit = st.sidebar.number_input("Annual Net Profit ($)", min_value=-1000000.0, value=50000.0, step=5000.0)

st.sidebar.header("🏗️ Assets & Valuation")
fixed_assets = st.sidebar.number_input("Fixed Assets Valuation ($)", min_value=0.0, value=200000.0)
inventory = st.sidebar.number_input("Inventory Value ($)", min_value=0.0, value=50000.0)
valuation = st.sidebar.number_input("Total Business Valuation ($)", min_value=0.0, value=1000000.0)
existing_debt = st.sidebar.number_input("Existing Debt ($)", min_value=0.0, value=100000.0)

st.sidebar.header("💰 Loan Request")
requested_amount = st.sidebar.number_input("Requested Loan Amount ($)", min_value=0.0, value=150000.0)

# Main Dashboard
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Assessment Context")
    st.info(f"""
    **Business Age:** {age} years  
    **Profit Margin:** {(profit/revenue*100):.2f}%  
    **Debt-to-Valuation:** {(existing_debt/valuation*100):.2f}%
    """)

if st.button("🚀 Run Credit Risk Analysis"):
    # Prepare API Request
    payload = {
        "age_years": int(age),
        "employees": int(employees),
        "is_franchise": int(is_franchise),
        "urban_rural": int(urban_rural),
        "annual_revenue": float(revenue),
        "net_profit": float(profit),
        "fixed_assets": float(fixed_assets),
        "inventory_value": float(inventory),
        "total_assets": float(fixed_assets + inventory + (revenue * 0.1)),
        "valuation": float(valuation),
        "existing_debt": float(existing_debt),
        "requested_amount": float(requested_amount)
    }
    
    try:
        response = requests.post("http://localhost:8000/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            
            with col2:
                st.subheader("Decision Results")
                
                if result['is_approved']:
                    st.success("✅ **STATUS: APPROVED**")
                else:
                    st.error("❌ **STATUS: REJECTED**")
                
                # Metrics
                m1, m2 = st.columns(2)
                m1.metric("Approval Prob.", f"{result['approval_probability']*100:.1f}%")
                m2.metric("Final Limit", f"${result['final_loan_recommendation']:,.0f}")
                
                st.divider()
                st.write("**Detailed Breakdown:**")
                st.write(f"- ML Recommended Limit: ${result['recommended_limit']:,.0f}")
                st.write(f"- Asset-Based Max Cap: ${result['max_allowable_loan']:,.0f}")
                st.write(f"- **Decision Logic:** {result['remarks']}")
                
        else:
            st.error(f"API Error: {response.text}")
    except Exception as e:
        st.error(f"Could not connect to Prediction API. Make sure the backend is running. Error: {e}")

st.markdown("---")
st.caption("Enterprise MSME Credit Risk Analysis")
