import streamlit as st
import pandas as pd

from services.auth import require_login
from services.ui import setup_page, sidebar
from services.customer_engine import get_model_data

setup_page("Customer Explorer")
if not require_login():
    st.stop()
sidebar()
df, *_ = get_model_data()

st.title("Customer Explorer")
st.markdown('<div class="page-subtitle">Search individual customers and inspect the behavioral and business indicators behind their segment.</div>', unsafe_allow_html=True)

query = st.text_input("Search Customer ID", value="CUST_00077")
filtered = df[df["Customer_ID"].astype(str).str.contains(query.strip(), case=False, na=False)] if query.strip() else df.copy()

st.markdown(f'<div class="small-label" style="margin:10px 0 10px">Showing {len(filtered):,} customers</div>', unsafe_allow_html=True)
preview_cols = ["Customer_ID", "Age", "Income_Level", "Product_Category", "Purchase_Amount", "Total_Purchases", "Customer_Value_Score", "Engagement_Score", "Loyalty_Score", "Churn_Risk_Score", "Segment"]
st.dataframe(filtered[preview_cols].head(100), use_container_width=True, hide_index=True)

ids = filtered["Customer_ID"].astype(str).tolist()
if ids:
    selected_id = st.selectbox("Select a customer for detailed profile", ids, index=0)
    customer = df[df["Customer_ID"].astype(str) == str(selected_id)].iloc[0]

    st.markdown("<hr style='border:0;border-top:1px solid #D8DEE7;margin:26px 0 36px;'>", unsafe_allow_html=True)
    st.header("Customer Profile")

    r1 = st.columns(4, gap="large")
    profile_values = [
        ("Customer ID", str(customer.Customer_ID)),
        ("Segment", str(customer.Segment)),
        ("Purchase Amount", f"₹{customer.Purchase_Amount:,.2f}"),
        ("Customer Value", f"{customer.Customer_Value_Score:.1f}/100"),
    ]
    for col, (label, value) in zip(r1, profile_values):
        with col:
            st.markdown(f'<div class="profile-label">{label}</div><div class="profile-value">{value}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    r2 = st.columns(4, gap="large")
    profile_values = [
        ("Age", f"{int(customer.Age)}"),
        ("Total Purchases", f"{int(customer.Total_Purchases)}"),
        ("Engagement", f"{customer.Engagement_Score:.1f}/100"),
        ("Churn Risk", f"{customer.Churn_Risk_Score:.1f}/100"),
    ]
    for col, (label, value) in zip(r2, profile_values):
        with col:
            st.markdown(f'<div class="profile-label">{label}</div><div class="profile-value">{value}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown(
        f'''<div class="detail-line">
            <b>Income Level:</b> {customer.Income_Level}<br>
            <b>Occupation:</b> {customer.Occupation}<br>
            <b>Education:</b> {customer.Education_Level}<br>
            <b>Location:</b> {customer.Location}<br>
            <b>Gender:</b> {customer.Gender}<br>
            <b>Product Category:</b> {customer.Product_Category}<br>
            <b>Payment Method:</b> {customer.Payment_Method}<br>
            <b>Reference Label:</b> {customer.Customer_Segment}
        </div>''', unsafe_allow_html=True,
    )
else:
    st.info("No customer matched the entered Customer ID.")
