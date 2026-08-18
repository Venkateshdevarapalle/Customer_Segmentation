import streamlit as st


def setup_page(title=None):
    st.set_page_config(
        page_title=title or "CustomerIQ",
        page_icon="◈",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        """
        <style>
        .stApp { background: #F7F9FC; }
        .block-container { padding-top: 1.25rem; padding-bottom: 2.5rem; max-width: 1400px; }
        [data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E3E7ED; }
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="stSidebar"] .block-container { padding: 1.45rem 0.9rem; }
        h1,h2,h3,h4 { color:#172033; letter-spacing:-0.02em; }
        h1 { font-size: 2rem; }
        h2 { font-size: 1.55rem; }
        h3 { font-size: 1.15rem; }
        .page-subtitle { color:#172033; font-size:1rem; margin-top:-0.35rem; margin-bottom:1.2rem; line-height:1.55; }
        .brand { font-size:1.35rem; font-weight:800; color:#172033; margin:0 0 2px 6px; }
        .brand-sub { font-size:.78rem; color:#64748B; margin:0 0 20px 6px; }
        .sidebar-link-note { color:#172033; font-size:.92rem; margin:0 0 10px 6px; }
        .kpi-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:16px; margin:12px 0 24px; }
        .kpi-card { background:#FFFFFF; border:1px solid #DDE3EA; border-radius:10px; padding:18px 20px; box-shadow:0 1px 4px rgba(15,23,42,.04); min-height:112px; }
        .kpi-label { font-size:.9rem; color:#172033; margin-bottom:8px; font-weight:500; }
        .kpi-value { font-size:1.7rem; font-weight:700; color:#172033; line-height:1.1; }
        .kpi-note { font-size:.78rem; color:#64748B; margin-top:7px; line-height:1.35; }
        .section-card { background:#FFFFFF; border:1px solid #DDE3EA; border-radius:10px; padding:18px 20px; box-shadow:0 1px 4px rgba(15,23,42,.035); }
        .info-card { background:#FFFFFF; border:1px solid #DDE3EA; border-radius:10px; padding:17px 18px; box-shadow:0 1px 4px rgba(15,23,42,.035); height:100%; }
        .segment-card { border:1px solid #DDE3EA; border-left:5px solid var(--accent); border-radius:16px; background:#FFFFFF; padding:24px 22px; min-height:320px; box-shadow:0 1px 5px rgba(15,23,42,.045); }
        .segment-title { font-size:1.18rem; font-weight:750; color:#172033; margin-bottom:5px; }
        .segment-count { color:#5F7393; font-size:.91rem; margin-bottom:8px; }
        .segment-desc { font-size:1rem; line-height:1.65; color:#172033; min-height:104px; }
        .metric { font-size:.92rem; margin:7px 0; color:#172033; }
        .metric b { font-weight:700; }
        .priority-card { background:#FFFFFF; border:1px solid #DDE3EA; border-radius:10px; padding:16px 17px; height:100%; box-shadow:0 1px 4px rgba(15,23,42,.035); }
        .priority-title { font-weight:700; color:#172033; margin-bottom:7px; }
        .priority-text { color:#5F7393; font-size:.88rem; line-height:1.5; }
        .priority-action { color:#172033; margin-top:14px; font-size:.9rem; line-height:1.5; }
        .result-card { background:#FFFFFF; border:1px solid #DDE3EA; border-left:5px solid var(--accent); border-radius:12px; padding:22px 24px; min-height:210px; box-shadow:0 1px 5px rgba(15,23,42,.04); }
        .result-kicker { color:#64748B; font-size:.78rem; font-weight:700; letter-spacing:.04em; }
        .result-name { color:#172033; font-size:1.65rem; font-weight:750; margin:7px 0 18px; }
        .result-confidence-label { color:#172033; font-size:.88rem; }
        .result-confidence { color:#172033; font-size:1.55rem; font-weight:700; margin-top:4px; }
        .result-why { color:#172033; font-size:.88rem; line-height:1.55; margin-top:14px; }
        .small-label { font-size:.8rem; color:#64748B; }
        .profile-value { font-size:1.55rem; color:#172033; font-weight:500; line-height:1.2; }
        .profile-label { font-size:.78rem; color:#172033; margin-bottom:5px; }
        .detail-line { font-size:.9rem; line-height:1.75; color:#172033; }
        .metric-card { background:#FFFFFF; border:1px solid #DDE3EA; border-radius:10px; padding:16px 17px; height:100%; }
        .metric-card-title { color:#64748B; font-size:.78rem; margin-bottom:7px; }
        .metric-card-value { color:#172033; font-size:1.45rem; font-weight:650; }
        .table-wrap { background:#FFFFFF; border:1px solid #DDE3EA; border-radius:10px; overflow:hidden; }
        .ai-card { background:#FFFFFF; border:1px solid #DDE3EA; border-radius:12px; padding:18px 18px; box-shadow:0 1px 4px rgba(15,23,42,.035); }
        .ai-label { font-weight:700; color:#172033; margin-bottom:7px; }
        .ai-body { color:#172033; line-height:1.55; }
        @media(max-width:1000px){.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
        @media(max-width:700px){.kpi-grid{grid-template-columns:1fr;}.segment-card{min-height:auto;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar():
    with st.sidebar:
        st.markdown('<div class="brand">Customer Segmentation</div><div class="brand-sub">AI-Powered Customer Intelligence</div>', unsafe_allow_html=True)
        st.page_link("pages/3_Customer_Prediction.py", label="Customer Prediction")
        st.page_link("app.py", label="Customer Intelligence")
        st.page_link("pages/1_Customer_Segments.py", label="Customer Segments")
        st.page_link("pages/2_Customer_Explorer.py", label="Customer Explorer")
        st.page_link("pages/4_Analytics.py", label="Analytics")
        st.page_link("pages/5_AI_Insights.py", label="AI Insights")
        st.page_link("pages/6_AI_Assistant.py", label="AI Assistant")
        st.page_link("pages/7_Model_Insights.py", label="Model Insights")
        st.page_link("pages/8_Data_Upload.py", label="Data Upload")


def kpi_grid(cards):
    html = '<div class="kpi-grid">'
    for label, value, note in cards:
        html += f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def segment_card(name, row, total):
    from services.customer_engine import SEGMENT_BORDERS, SEGMENT_DESCRIPTIONS
    st.markdown(
        f'''<div class="segment-card" style="--accent:{SEGMENT_BORDERS[name]}">
            <div class="segment-title">{name}</div>
            <div class="segment-count">{int(row.customers):,} customers · {row.percentage:.1f}%</div>
            <div class="segment-desc">{SEGMENT_DESCRIPTIONS[name]}</div>
            <div class="metric"><b>Avg spending:</b> ₹{row.avg_spending:,.0f}</div>
            <div class="metric"><b>Frequency:</b> {row.frequency:.1f}</div>
            <div class="metric"><b>Customer value:</b> {row.customer_value:.1f}/100</div>
            <div class="metric"><b>Churn risk:</b> {row.churn_risk:.1f}/100</div>
        </div>''',
        unsafe_allow_html=True,
    )
