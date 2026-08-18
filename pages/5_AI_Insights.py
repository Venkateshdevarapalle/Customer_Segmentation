import streamlit as st

from services.auth import require_login
from services.ui import setup_page, sidebar
from services.customer_engine import get_model_data, segment_summary, SEGMENT_ORDER, SEGMENT_DESCRIPTIONS

setup_page("AI Insights")
if not require_login():
    st.stop()
sidebar()
df, *_ = get_model_data()
summary = segment_summary(df)

st.title("AI Insights")
st.markdown('<div class="page-subtitle">AI-assisted explanations built from verified ML segment statistics. The AI layer does not invent clustering results.</div>', unsafe_allow_html=True)
selected = st.selectbox("Select a discovered segment", SEGMENT_ORDER)
row = summary.loc[selected]
selected_df = df[df["Segment"] == selected]

actions = {
    "At-Risk": "Prioritize a win-back campaign, ask for feedback, and reduce friction before pushing high-value upsells.",
    "Budget": "Use value packs and low-risk cross-sell offers to improve conversion.",
    "Potential": "Promote relevant bundles and repeat-purchase incentives.",
    "Premium / High-Value": "Launch loyalty and personalized-value offers.",
    "Regular": "Maintain consistent engagement and introduce relevant cross-sell opportunities.",
}

st.markdown(
    f'''<div class="ai-card">
        <h2 style="margin-top:0">{selected}</h2>
        <div class="ai-label">Insight</div>
        <div class="ai-body">{SEGMENT_DESCRIPTIONS[selected]}</div>
        <div style="height:16px"></div>
        <div class="ai-label">Verified evidence</div>
        <div class="ai-body">{int(row.customers):,} customers · ₹{row.avg_spending:,.0f} avg spending · {selected_df.Engagement_Score.mean():.1f}/100 engagement · {selected_df.Loyalty_Score.mean():.1f}/100 loyalty · {selected_df.Churn_Risk_Score.mean():.1f}/100 churn risk</div>
        <div style="height:16px"></div>
        <div class="ai-label">Recommended action</div>
        <div class="ai-body">{actions[selected]}</div>
    </div>''', unsafe_allow_html=True,
)

st.header("Executive Priorities")
priorities = [
    ("Retain high-value customers", f"Premium group averages {summary.loc['Premium / High-Value','customer_value']:.1f}/100 customer value.", "Launch loyalty and personalized-value offers."),
    ("Re-engage at-risk customers", f"At-Risk group has {summary.loc['At-Risk','churn_risk']:.1f}/100 average churn risk.", "Use win-back messages and friction-reduction offers."),
    ("Grow potential customers", f"Potential group has {summary.loc['Potential','engagement']:.1f}/100 average engagement.", "Promote relevant bundles and repeat-purchase incentives."),
    ("Improve budget conversion", f"Budget group averages ₹{summary.loc['Budget','avg_spending']:,.0f} spending per purchase.", "Use value packs and low-risk cross-sell offers."),
]
for title, evidence, action in priorities:
    st.markdown(f'<div style="margin:0 0 14px 0; color:#172033; font-size:.95rem; line-height:1.6">• &nbsp;<b>{title}</b> — {evidence} <b>Action:</b> {action}</div>', unsafe_allow_html=True)
