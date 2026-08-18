import streamlit as st
import pandas as pd
import plotly.express as px

from services.auth import require_login
from services.ui import setup_page, sidebar
from services.customer_engine import get_model_data, segment_summary, SEGMENT_ORDER, SEGMENT_COLORS_HEX

setup_page("Analytics")
if not require_login():
    st.stop()
sidebar()
df, *_ = get_model_data()
summary = segment_summary(df)

st.title("Analytics")
st.markdown('<div class="page-subtitle">Simple business views for spending, engagement, customer value and category behavior.</div>', unsafe_allow_html=True)

metrics = st.multiselect(
    "Select segment metrics",
    ["Avg Spending", "Customer Value", "Engagement"],
    default=["Avg Spending", "Customer Value", "Engagement"],
)

metric_map = {"Avg Spending": "avg_spending", "Customer Value": "customer_value", "Engagement": "engagement"}
metric_data = []
for metric in metrics:
    col = metric_map[metric]
    vals = summary[col].copy()
    if metric == "Avg Spending":
        vals = vals / summary["avg_spending"].max() * 100
    else:
        vals = vals
    for segment, value in vals.items():
        metric_data.append({"Segment": segment, "Metric": metric, "Score": value})
metric_df = pd.DataFrame(metric_data)

if not metric_df.empty:
    fig = px.bar(metric_df, x="Segment", y="Score", color="Metric", barmode="group", category_orders={"Segment": SEGMENT_ORDER}, labels={"Score":"Relative score (0-100)", "Segment":""}, color_discrete_sequence=["#0B70C9", "#7FC3F2", "#FF2D2D"])
    fig.update_layout(height=350, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC", legend_title="", yaxis=dict(range=[0,100]))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

left, right = st.columns(2, gap="large")
with left:
    st.subheader("Customer Value vs Spending")
    sample = df.sample(min(1800, len(df)), random_state=42)
    fig = px.scatter(sample, x="Customer_Value_Score", y="Purchase_Amount", color="Segment", color_discrete_map=SEGMENT_COLORS_HEX, labels={"Customer_Value_Score":"Customer Value Score", "Purchase_Amount":"Spending"})
    fig.update_traces(marker=dict(size=5, opacity=.65))
    fig.update_layout(height=320, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC", legend_title="Segment")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with right:
    st.subheader("Product Category Mix")
    cats = df["Product_Category"].value_counts().sort_values(ascending=False).reset_index()
    cats.columns = ["Category", "Customers"]
    fig = px.bar(cats, x="Category", y="Customers", labels={"Customers":"Customers", "Category":"Category"})
    fig.update_traces(marker_color="#0B70C9")
    fig.update_layout(height=320, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC", xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.subheader("Segment Performance Table")
table = summary.copy()
table["Customers"] = table["customers"].astype(int)
table["Avg Spending"] = table["avg_spending"].map(lambda x: f"₹{x:,.0f}")
table["Avg Order Value"] = df.groupby("Segment")["Average_Order_Value"].mean().reindex(SEGMENT_ORDER).map(lambda x: f"₹{x:,.0f}")
table["Frequency"] = table["frequency"].map(lambda x: f"{x:.1f}")
table["Engagement"] = df.groupby("Segment")["Engagement_Score"].mean().reindex(SEGMENT_ORDER).map(lambda x: f"{x:.1f}")
table["Loyalty"] = df.groupby("Segment")["Loyalty_Score"].mean().reindex(SEGMENT_ORDER).map(lambda x: f"{x:.1f}")
table["Churn Risk"] = table["churn_risk"].map(lambda x: f"{x:.1f}")
table["Customer Value"] = table["customer_value"].map(lambda x: f"{x:.1f}")
table = table.reset_index()[["Segment", "Customers", "Avg Spending", "Avg Order Value", "Frequency", "Engagement", "Loyalty", "Churn Risk", "Customer Value"]]
st.dataframe(table, use_container_width=True, hide_index=True)
