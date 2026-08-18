import streamlit as st
import pandas as pd
import plotly.express as px

from services.auth import require_login
from services.ui import setup_page, sidebar, segment_card
from services.customer_engine import get_model_data, segment_summary, SEGMENT_ORDER, category_counts

setup_page("Customer Segments")
if not require_login():
    st.stop()
sidebar()
df, *_ = get_model_data()
summary = segment_summary(df)

st.title("Customer Segments")
st.markdown('<div class="page-subtitle">Explore the behavioral groups discovered by the K-Means model.</div>', unsafe_allow_html=True)

# Keep the exact three-card + two-card arrangement from the reference.
cols = st.columns(3, gap="large")
for i, name in enumerate(SEGMENT_ORDER[:3]):
    with cols[i]:
        segment_card(name, summary.loc[name], len(df))

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
cols2 = st.columns(3, gap="large")
for i, name in enumerate(SEGMENT_ORDER[3:]):
    with cols2[i]:
        segment_card(name, summary.loc[name], len(df))

st.markdown("<hr style='border:0;border-top:1px solid #D8DEE7;margin:28px 0 36px;'>", unsafe_allow_html=True)
st.header("Segment Detail")
selected = st.selectbox("Select a segment to explore", SEGMENT_ORDER)
row = summary.loc[selected]
selected_df = df[df["Segment"] == selected]

# View the complete customer details for the selected segment without disturbing the existing detail layout.
view_segment = st.button("View Segment Customers", key="view_segment_customers")
if view_segment:
    st.session_state["show_segment_customers"] = True

if st.session_state.get("show_segment_customers", False):
    st.markdown(f"**Customers in {selected}**")
    detail_cols = [
        "Customer_ID", "Transaction_ID", "Purchase_Date", "Age", "Gender", "Income_Level",
        "Occupation", "Education_Level", "Location", "Product_Category", "Payment_Method",
        "Purchase_Amount", "Total_Purchases", "Average_Order_Value", "Repeat_Purchase_Rate",
        "Browsing_Frequency", "Engagement_Score", "Loyalty_Score", "Churn_Risk_Score",
        "Customer_Value_Score", "Segment"
    ]
    detail_cols = [c for c in detail_cols if c in selected_df.columns]
    st.dataframe(selected_df[detail_cols], use_container_width=True, hide_index=True)
    if st.button("Hide Segment Customers", key="hide_segment_customers"):
        st.session_state["show_segment_customers"] = False
        st.rerun()

# Detail metrics
m1, m2, m3, m4, m5 = st.columns(5, gap="large")
for col, label, value in [
    (m1, "Customers", f"{int(row.customers):,}"),
    (m2, "Avg Age", f"{selected_df.Age.mean():.0f}"),
    (m3, "Avg Spending", f"₹{row.avg_spending:,.0f}"),
    (m4, "Avg Order Value", f"₹{selected_df.Average_Order_Value.mean():,.0f}"),
    (m5, "Frequency", f"{row.frequency:.1f}/customer"),
]:
    with col:
        st.markdown(f'<div class="profile-label">{label}</div><div class="profile-value">{value}</div>', unsafe_allow_html=True)

st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
m6, m7, m8, m9 = st.columns(4, gap="large")
for col, label, value in [
    (m6, "Engagement", f"{selected_df.Engagement_Score.mean():.1f}/100"),
    (m7, "Loyalty", f"{selected_df.Loyalty_Score.mean():.1f}/100"),
    (m8, "Churn Risk", f"{selected_df.Churn_Risk_Score.mean():.1f}/100"),
    (m9, "Customer Value", f"{selected_df.Customer_Value_Score.mean():.1f}/100"),
]:
    with col:
        st.markdown(f'<div class="profile-label">{label}</div><div class="profile-value">{value}</div>', unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
left, right = st.columns(2, gap="large")
with left:
    st.subheader("Behavioral Profile")
    profile = pd.DataFrame({
        "Metric": ["Churn Risk", "Customer Value", "Engagement", "Loyalty"],
        "Score": [selected_df.Churn_Risk_Score.mean(), selected_df.Customer_Value_Score.mean(), selected_df.Engagement_Score.mean(), selected_df.Loyalty_Score.mean()],
    })
    fig = px.bar(profile, x="Metric", y="Score", labels={"Score":"", "Metric":""})
    fig.update_traces(marker_color="#0B70C9")
    fig.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC", yaxis=dict(range=[0, 65]))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with right:
    st.subheader("Preferred Categories")
    cats = category_counts(df, selected).reset_index()
    cats.columns = ["Category", "Customers"]
    fig = px.bar(cats, x="Category", y="Customers", labels={"Customers":"Customers", "Category":"Category"})
    fig.update_traces(marker_color="#0B70C9")
    fig.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC", xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.subheader("Customer Value Distribution")
fig = px.histogram(selected_df, x="Customer_Value_Score", nbins=12, labels={"Customer_Value_Score":"Customer Value Score", "count":"Customers"})
fig.update_traces(marker_color="#0B70C9")
fig.update_layout(height=310, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC", showlegend=False)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown(
    f'''<div class="section-card">
        <div class="ai-label">Why does this segment matter?</div>
        <div class="ai-body">{__import__('services.customer_engine', fromlist=['SEGMENT_DESCRIPTIONS']).SEGMENT_DESCRIPTIONS[selected]}</div>
        <div style="height:18px"></div>
        <div class="ai-label">What should the business do?</div>
        <div class="ai-body">{ {
            "At-Risk": "Prioritize a win-back campaign, ask for feedback, and reduce friction.",
            "Budget": "Use value packs and low-risk cross-sell offers to improve conversion.",
            "Potential": "Promote relevant bundles and repeat-purchase incentives.",
            "Premium / High-Value": "Launch loyalty and personalized-value offers.",
            "Regular": "Maintain consistent engagement and introduce relevant cross-sell opportunities.",
        }[selected]}</div>
    </div>''', unsafe_allow_html=True,
)
