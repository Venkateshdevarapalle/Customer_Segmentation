import streamlit as st
import pandas as pd
import plotly.express as px

from services.auth import require_login
from services.ui import setup_page, sidebar
from services.customer_engine import predict_segment, INCOME_RANGES, SEGMENT_COLORS_HEX, SEGMENT_ORDER

setup_page("Customer Prediction")
if not require_login():
    st.stop()
sidebar()

st.title("Predict Customer Segment")
st.markdown('<div class="page-subtitle">Enter a new customer\'s characteristics to estimate the closest discovered behavioral segment.</div>', unsafe_allow_html=True)
st.markdown('<div class="small-label" style="margin-bottom:16px">Prediction uses the trained K-Means model. Income levels come from the finalized dataset and are displayed with clear lakh ranges so the categorical input is easy to understand.</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    age = st.number_input("Age", min_value=18, max_value=100, value=43, step=1)
    income_options = [f"₹{lo:g}–{hi:g} lakh" for lo, hi in INCOME_RANGES.values()]
    income_choice = st.selectbox("Income Level", income_options, index=2)
    income_level = list(INCOME_RANGES.keys())[income_options.index(income_choice)]
    lo, hi = INCOME_RANGES[income_level]
    income = (lo + hi) / 2
with c2:
    spending = st.number_input("Annual Purchase Amount / Spending (₹)", min_value=0.0, max_value=1000000000.0, value=14500.0, step=500.0)
    aov = st.number_input("Average Order Value (₹)", min_value=0.0, max_value=50000.0, value=7500.0, step=250.0)

annual_income_max = hi * 100000
if spending > annual_income_max:
    st.warning("NOTE : annual purchase amount is more than the income")

if st.button("Predict Segment", type="primary", use_container_width=True):
    segment, confidence, centroids, probabilities = predict_segment(age, income, spending, aov)
    left, right = st.columns([0.42, 0.58], gap="large")
    with left:
        border = SEGMENT_COLORS_HEX[segment]
        st.markdown(
            f'''<div class="result-card" style="--accent:{border}">
                <div class="result-kicker">PREDICTED SEGMENT</div>
                <div class="result-name">{segment}</div>
                <div class="result-confidence-label">Model confidence</div>
                <div class="result-confidence">{confidence*100:.1f}%</div>
                <div class="result-why">The result is based on distance to the five learned K-Means centroids.</div>
            </div>''', unsafe_allow_html=True,
        )
    with right:
        st.subheader("Segment Probability Scores")
        chart = pd.DataFrame({"Segment": SEGMENT_ORDER, "Probability": [probabilities[s] for s in SEGMENT_ORDER]})
        fig = px.bar(chart, x="Segment", y="Probability", labels={"Probability":"Probability (%)", "Segment":""}, color="Segment", color_discrete_map=SEGMENT_COLORS_HEX)
        fig.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC", showlegend=False, yaxis=dict(range=[0, max(50, chart.Probability.max() * 1.2)]))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
