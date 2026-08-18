import streamlit as st

from services.auth import require_login
from services.ui import setup_page, sidebar
from services.customer_engine import get_model_data, segment_summary, SEGMENT_ORDER

setup_page("Model Insights")
if not require_login():
    st.stop()
sidebar()
df, model, scaler, mapping, metrics, *_ = get_model_data()
summary = segment_summary(df)

st.title("Model Insights")
st.markdown('<div class="page-subtitle">Technical details of the clustering model powering CustomerIQ segmentation.</div>', unsafe_allow_html=True)

cards = [
    ("Algorithm", "K-Means", "behavioral clustering"),
    ("Number of Clusters", "5", "business segments"),
    ("Features Used", "7", "model input features"),
    ("Silhouette Score", f"{metrics['silhouette']:.3f}", "higher is better"),
    ("Davies-Bouldin Index", f"{metrics['davies_bouldin']:.3f}", "lower is better"),
    ("Calinski-Harabasz", f"{metrics['calinski_harabasz']:,.1f}", "cluster separation"),
    ("Dataset Size", f"{len(df):,}", "customers"),
    ("Model Status", "Trained", "finalized dataset"),
]
html = '<div class="kpi-grid">'
for label, value, note in cards:
    html += f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>'
html += '</div>'
st.markdown(html, unsafe_allow_html=True)

st.header("Evaluation Metrics")
eval_df = __import__("pandas").DataFrame([{
    "Algorithm": "K-Means",
    "Clusters": 5,
    "Features": 7,
    "Silhouette Score": metrics["silhouette"],
    "Davies-Bouldin Index": metrics["davies_bouldin"],
    "Calinski-Harabasz Score": metrics["calinski_harabasz"],
}])
st.dataframe(eval_df, use_container_width=True, hide_index=True)

st.header("Cluster Profiles")
profiles = summary.copy()
profiles["Customers"] = profiles["customers"].astype(int)
profiles["Avg Spending"] = profiles["avg_spending"].map(lambda x: f"₹{x:,.2f}")
profiles["Avg Order Value"] = df.groupby("Segment")["Average_Order_Value"].mean().reindex(SEGMENT_ORDER).map(lambda x: f"₹{x:,.2f}")
profiles["Frequency"] = profiles["frequency"].map(lambda x: f"{x:.2f}")
profiles["Engagement"] = df.groupby("Segment")["Engagement_Score"].mean().reindex(SEGMENT_ORDER).map(lambda x: f"{x:.2f}")
profiles["Loyalty"] = df.groupby("Segment")["Loyalty_Score"].mean().reindex(SEGMENT_ORDER).map(lambda x: f"{x:.2f}")
profiles["Churn Risk"] = profiles["churn_risk"].map(lambda x: f"{x:.2f}")
profiles["Customer Value"] = profiles["customer_value"].map(lambda x: f"{x:.2f}")
profiles = profiles.reset_index()[["Segment", "Customers", "Avg Spending", "Avg Order Value", "Frequency", "Engagement", "Loyalty", "Churn Risk", "Customer Value"]]
st.dataframe(profiles, use_container_width=True, hide_index=True)

st.markdown(
    '<div class="section-card" style="margin-top:22px"><h3 style="margin-top:0">Features used</h3><p style="margin-bottom:0">Purchase Amount · Total Purchases · Average Order Value · Engagement Score · Loyalty Score · Churn Risk Score · Customer Value Score</p></div>',
    unsafe_allow_html=True,
)
