import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime
import re

from services.auth import require_login
from services.ui import setup_page, sidebar
from services.customer_engine import (
    get_model_data,
    MODEL_FEATURES,
    MODEL_FEATURE_WEIGHTS,
    SEGMENT_ORDER,
    SEGMENT_COLORS_HEX,
)
from services.database import log_upload

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def _safe_upload_name(name):
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(name).stem).strip("._") or "dataset"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{stamp}_{stem}.csv"

setup_page("Data Upload")
if not require_login():
    st.stop()
sidebar()
st.title("Data Upload")
st.markdown('<div class="page-subtitle">Upload a customer dataset (CSV) and review its data quality before using it.</div>', unsafe_allow_html=True)
file = st.file_uploader("Upload customer dataset (CSV)", type=["csv"])

if file:
    # Store the upload as an independent file. It is NEVER appended to,
    # merged with, or used to replace the finalized project dataset.
    saved_path = UPLOAD_DIR / _safe_upload_name(file.name)
    saved_path.write_bytes(file.getvalue())
    df_upload = pd.read_csv(saved_path)
    st.caption(f"Stored separately as: data/uploads/{saved_path.name}")
    st.success(f"Loaded {len(df_upload):,} rows and {len(df_upload.columns)} columns.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{len(df_upload):,}")
    c2.metric("Columns", len(df_upload.columns))
    c3.metric("Missing values", int(df_upload.isna().sum().sum()))
    st.dataframe(df_upload.head(50), use_container_width=True, hide_index=True)

    missing = [c for c in MODEL_FEATURES if c not in df_upload.columns]
    if missing:
        log_upload(file.name, len(df_upload), len(df_upload.columns), False)
        st.warning("The uploaded dataset cannot be segmented because these required model fields are missing: " + ", ".join(missing))
    else:
        st.subheader("Uploaded Dataset Segmentation")
        _, model, scaler, mapping, _, *_ = get_model_data()
        X = df_upload[MODEL_FEATURES].apply(pd.to_numeric, errors="coerce")
        X = X.fillna(pd.Series({c: pd.to_numeric(df_upload[c], errors="coerce").median() for c in MODEL_FEATURES}))
        X_scaled = scaler.transform(X) * MODEL_FEATURE_WEIGHTS
        labels = model.predict(X_scaled)
        df_upload["Uploaded_Segment"] = pd.Series(labels, index=df_upload.index).map(mapping)
        log_upload(file.name, len(df_upload), len(df_upload.columns), True)

        seg_counts = df_upload["Uploaded_Segment"].value_counts().reindex(SEGMENT_ORDER).fillna(0).astype(int).reset_index()
        seg_counts.columns = ["Segment", "Customers"]
        seg_counts["Percentage"] = seg_counts["Customers"] / len(df_upload) * 100
        st.dataframe(seg_counts, use_container_width=True, hide_index=True)

        fig = px.bar(
            seg_counts,
            x="Segment",
            y="Customers",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS_HEX,
            category_orders={"Segment": SEGMENT_ORDER},
        )
        fig.update_layout(height=330, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#F7F9FC", plot_bgcolor="#F7F9FC", showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        if "Customer_ID" in df_upload.columns:
            profile_view = df_upload.groupby("Uploaded_Segment").agg(
                Customers=("Customer_ID", "count"),
                Avg_Spending=("Purchase_Amount", "mean"),
                Avg_Order_Value=("Average_Order_Value", "mean"),
                Engagement=("Engagement_Score", "mean"),
                Loyalty=("Loyalty_Score", "mean"),
                Churn_Risk=("Churn_Risk_Score", "mean"),
                Customer_Value=("Customer_Value_Score", "mean"),
            ).reindex(SEGMENT_ORDER).reset_index()
            st.dataframe(profile_view, use_container_width=True, hide_index=True)
else:
    st.info("No file uploaded yet. Upload a CSV to see a data-quality report and preview.")
