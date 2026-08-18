import streamlit as st

from services.auth import require_login
from services.ui import setup_page, sidebar
from services.customer_engine import get_model_data, segment_summary
from services.ai_service import answer_question

setup_page("AI Assistant")
if not require_login():
    st.stop()
sidebar()
df, *_ = get_model_data()
summary = segment_summary(df)

st.title("Ask CustomerIQ")
st.markdown('<div class="page-subtitle">Ask questions about your customer segments and business performance.</div>', unsafe_allow_html=True)
st.markdown('<div class="small-label" style="margin-bottom:16px">Answers are generated from verified dataset and model statistics, so they remain grounded in the project data.</div>', unsafe_allow_html=True)

questions = [
    "Which segment has the highest spending?",
    "Which customers should we target for retention?",
    "Why is the Premium segment valuable?",
    "Which segment has the highest engagement?",
    "What category does the Potential segment prefer?",
    "How does CustomerIQ create segments?",
]

answers = {
    questions[0]: f"{summary['avg_spending'].idxmax()} has the highest average spending at approximately ₹{summary['avg_spending'].max():,.0f} per purchase.",
    questions[1]: f"{summary['churn_risk'].idxmax()} customers should be the main retention priority because their average churn risk is {summary['churn_risk'].max():.1f}/100.",
    questions[2]: f"Premium / High-Value is valuable because it has the strongest average customer value ({summary.loc['Premium / High-Value','customer_value']:.1f}/100) and high spending (₹{summary.loc['Premium / High-Value','avg_spending']:,.0f}).",
    questions[3]: f"{summary['engagement'].idxmax()} has the highest average engagement at {summary['engagement'].max():.1f}/100.",
    questions[4]: f"The most common product category among Potential customers is {df[df['Segment'] == 'Potential']['Product_Category'].value_counts().idxmax()}.",
    questions[5]: "CustomerIQ uses K-Means clustering on seven behavioral and value features, with scaling and feature weighting, then assigns business-friendly names to five discovered clusters based on their profiles.",
}

cols = st.columns(3, gap="medium")
for i, question in enumerate(questions):
    with cols[i % 3]:
        if st.button(question, key=f"q{i}", use_container_width=True):
            st.session_state["assistant_answer"] = answers[question]

if "assistant_answer" in st.session_state:
    st.markdown('<div style="height:22px"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ai-card"><div class="ai-label">CustomerIQ</div><div class="ai-body">{st.session_state["assistant_answer"]}</div></div>', unsafe_allow_html=True)

custom = st.chat_input("Ask a question about your customers or segments...")
if custom:
    answer, _ = answer_question(custom, df, summary)
    st.session_state["assistant_answer"] = answer
    st.rerun()
