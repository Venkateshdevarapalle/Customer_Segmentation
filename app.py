import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from services.auth import require_login
from services.ui import setup_page, sidebar, kpi_grid
from services.customer_engine import get_model_data, segment_summary, SEGMENT_ORDER, SEGMENT_COLORS_HEX

setup_page("Customer Intelligence")
if not require_login():
    st.stop()
sidebar()
df, *_ = get_model_data()
summary = segment_summary(df)

st.title("Customer Intelligence Overview")
st.markdown(
    '<div class="page-subtitle">Understand your customers, discover meaningful segments, and turn behavioral data into clear business decisions.</div>',
    unsafe_allow_html=True,
)

high_value = int((df["Customer_Value_Score"] >= 70).sum())
at_risk = int((df["Churn_Risk_Score"] >= 70).sum())

kpi_grid([
    ("Total Customers", f"{len(df):,}", "records in the finalized dataset"),
    ("Customer Segments", "5", "K-Means behavioral segmentation"),
    ("Avg Customer Value", f"{df.Customer_Value_Score.mean():.1f}/100", "dataset customer-value score"),
    ("Avg Spending", f"₹{df.Purchase_Amount.mean():,.0f}", "average purchase amount"),
    ("Avg Purchase Frequency", f"{df.Total_Purchases.mean():.1f}", "purchases per customer"),
    ("High-Value Customers", f"{high_value:,}", "customer-value score ≥ 70"),
    ("At-Risk Customers", f"{at_risk:,}", "churn-risk score ≥ 70"),
    ("Engagement Score", f"{df.Engagement_Score.mean():.1f}/100", "average engagement score"),
])

# Customer Segment Distribution + Customer Value vs. Spending
left, right = st.columns([1, 1], gap="large")
with left:
    st.subheader("Customer Segment Distribution")
    donut = summary.reset_index()
    donut["Segment"] = donut["Segment"].astype(str)
    fig = go.Figure(
        data=[go.Pie(
            labels=donut["Segment"],
            values=donut["customers"],
            hole=0.48,
            sort=False,
            direction="clockwise",
            marker=dict(colors=[SEGMENT_COLORS_HEX[s] for s in donut["Segment"]], line=dict(color="#FFFFFF", width=1)),
            texttemplate="%{label}<br>%{percent}",
            textposition="outside",
            hovertemplate="%{label}<br>%{value:,} customers<br>%{percent}<extra></extra>",
        )]
    )
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), showlegend=True, legend=dict(orientation="v"), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with right:
    st.subheader("Customer Value vs. Spending")
    sample = df.sample(min(1800, len(df)), random_state=42)
    fig = px.scatter(
        sample,
        x="Customer_Value_Score",
        y="Purchase_Amount",
        color="Segment",
        color_discrete_map=SEGMENT_COLORS_HEX,
        labels={"Customer_Value_Score": "Customer Value Score", "Purchase_Amount": "Spending"},
        hover_data=["Customer_ID", "Age", "Income_Level"],
    )
    fig.update_traces(marker=dict(size=5, opacity=0.65))
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC", legend_title="Segment")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# Segment Performance
st.subheader("Segment Performance")
perf = summary.reset_index()
perf = perf.melt(id_vars=["Segment"], value_vars=["avg_spending", "customer_value", "engagement"], var_name="Metric", value_name="Score")
perf["Metric"] = perf["Metric"].map({"avg_spending": "Avg Spending", "customer_value": "Customer Value", "engagement": "Engagement"})
# Scale spending to the 0-100 range so the three business indicators can be read together.
spending_max = summary["avg_spending"].max()
perf.loc[perf["Metric"] == "Avg Spending", "Score"] = perf.loc[perf["Metric"] == "Avg Spending", "Score"] / spending_max * 100
fig = px.bar(perf, x="Segment", y="Score", color="Metric", barmode="group", category_orders={"Segment": SEGMENT_ORDER}, labels={"Score": "Relative score (0-100)", "Segment": ""}, color_discrete_sequence=["#0B70C9", "#7FC3F2", "#FF2D2D"])
fig.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC", legend_title="", yaxis=dict(range=[0, 100]))
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# AI Executive Summary
st.subheader("AI Executive Summary")
premium_value = summary.loc["Premium / High-Value", "customer_value"]
at_risk_churn = summary.loc["At-Risk", "churn_risk"]
potential_engagement = summary.loc["Potential", "engagement"]
budget_spending = summary.loc["Budget", "avg_spending"]
st.markdown(
    f'<div class="section-card">CustomerIQ identified five behavioral groups from {len(df):,} customer records. Premium / High-Value customers show the strongest value signals and should be protected, while At-Risk customers show higher churn risk ({at_risk_churn:.1f}/100) and deserve retention attention. The segmentation is exploratory rather than a ground-truth classifier, so business actions are based on verified segment statistics.</div>',
    unsafe_allow_html=True,
)

st.subheader("Recommended Priorities")
priorities = [
    ("Retain high-value customers", f"Premium group averages {premium_value:.1f}/100 customer value.", "Launch loyalty and personalized-value offers."),
    ("Re-engage at-risk customers", f"At-Risk group has {at_risk_churn:.1f}/100 average churn risk.", "Use win-back messages and friction-reduction offers."),
    ("Grow potential customers", f"Potential group has {potential_engagement:.1f}/100 average engagement.", "Promote relevant bundles and repeat-purchase incentives."),
    ("Improve budget conversion", f"Budget group averages ₹{budget_spending:,.0f} spending per purchase.", "Use value packs and low-risk cross-sell offers."),
]
cols = st.columns(4, gap="medium")
for col, (title, body, action) in zip(cols, priorities):
    with col:
        st.markdown(f'<div class="priority-card"><div class="priority-title">{title}</div><div class="priority-text">{body}</div><div class="priority-action"><b>Action:</b> {action}</div></div>', unsafe_allow_html=True)
