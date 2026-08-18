"""Grounded CustomerIQ assistant.

The assistant answers from the finalized CustomerIQ dataframe and verified model
statistics. Exact customer/data questions are resolved locally first, so the
application works without an external API key. An optional OpenAI fallback can
handle natural-language questions that are not covered by the deterministic
query layer, while being explicitly instructed to stay inside verified context.
"""
from __future__ import annotations

import os
import re
from typing import Optional

import pandas as pd


def _normalize_customer_id(text: str) -> Optional[str]:
    match = re.search(r"\bCUST[_\- ]?\d+\b", text, flags=re.IGNORECASE)
    if not match:
        return None
    value = match.group(0).upper().replace("-", "_").replace(" ", "_")
    if value.startswith("CUST") and not value.startswith("CUST_"):
        value = "CUST_" + value[4:]
    return value


def _fmt_number(value) -> str:
    value = float(value)
    return f"{value:,.2f}" if value % 1 else f"{value:,.0f}"


def _fmt_value(column: str, value) -> str:
    if pd.isna(value):
        return "not available"
    if column in {"Purchase_Amount", "Average_Order_Value"}:
        return f"₹{float(value):,.2f}"
    if column.endswith("_Score") or column in {"Repeat_Purchase_Rate", "Bounce_Rate", "Click_Through_Rate", "Email_Open_Rate", "Response_Rate"}:
        # Existing score fields are already 0-100 in CustomerIQ; the three
        # rate fields in this dataset are also represented numerically.
        return f"{float(value):.1f}/100"
    if column in {"Total_Purchases", "Age", "Pages_Visited", "Ad_Clicks", "Product_Link_Clicks", "Chatbot_Interactions"}:
        return _fmt_number(value)
    return str(value)


def _customer_lookup(question: str, df: pd.DataFrame):
    """Answer customer-specific questions directly from the verified dataframe."""
    customer_id = _normalize_customer_id(question)
    if not customer_id:
        return None

    rows = df[df["Customer_ID"].astype(str).str.upper() == customer_id]
    if rows.empty:
        return f"I could not find {customer_id} in the finalized customer dataset."

    row = rows.iloc[0]
    q = question.lower()

    field_map = [
        (("age",), "Age"),
        (("income",), "Income_Level"),
        (("product category", "category", "product"), "Product_Category"),
        (("purchase amount", "spending", "spent", "annual purchase"), "Purchase_Amount"),
        (("average order", "order value", "aov"), "Average_Order_Value"),
        (("total purchase", "purchases", "frequency"), "Total_Purchases"),
        (("customer value",), "Customer_Value_Score"),
        (("engagement",), "Engagement_Score"),
        (("loyalty",), "Loyalty_Score"),
        (("churn", "risk"), "Churn_Risk_Score"),
        (("segment", "cluster"), "Segment"),
        (("occupation", "job"), "Occupation"),
        (("education",), "Education_Level"),
        (("location", "city", "area"), "Location"),
        (("gender",), "Gender"),
        (("payment",), "Payment_Method"),
        (("purchase date", "date", "bought"), "Purchase_Date"),
        (("repeat purchase",), "Repeat_Purchase_Rate"),
        (("session",), "Session_Duration"),
        (("pages",), "Pages_Visited"),
        (("bounce",), "Bounce_Rate"),
        (("browsing",), "Browsing_Frequency"),
        (("click through", "ctr"), "Click_Through_Rate"),
        (("feedback",), "Feedback_Score"),
        (("support request",), "Support_Request_Frequency"),
    ]

    for terms, column in field_map:
        if column in row.index and any(term in q for term in terms):
            label = column.replace("_", " ").lower()
            return f"{customer_id}'s {label} is {_fmt_value(column, row[column])}."

    # General customer profile request.
    profile_fields = [
        ("Age", "age"), ("Income_Level", "income level"),
        ("Product_Category", "product category"), ("Purchase_Amount", "purchase amount"),
        ("Total_Purchases", "total purchases"), ("Average_Order_Value", "average order value"),
        ("Customer_Value_Score", "customer value"), ("Engagement_Score", "engagement"),
        ("Loyalty_Score", "loyalty"), ("Churn_Risk_Score", "churn risk"),
        ("Segment", "segment"), ("Occupation", "occupation"),
        ("Location", "location"), ("Gender", "gender"),
    ]
    parts = []
    for column, label in profile_fields:
        if column in row.index:
            parts.append(f"{label}: {_fmt_value(column, row[column])}")
    return f"Here is the verified profile for {customer_id}: " + "; ".join(parts) + "."


def _segment_from_question(question: str, summary: pd.DataFrame):
    q = question.lower()
    for segment in summary.index:
        if segment.lower() in q:
            return segment
    aliases = {
        "premium": "Premium / High-Value",
        "high value": "Premium / High-Value",
        "high-value": "Premium / High-Value",
        "at risk": "At-Risk",
        "at-risk": "At-Risk",
    }
    for alias, segment in aliases.items():
        if alias in q:
            return segment
    return None


def _column_from_question(question: str):
    q = question.lower()
    aliases = {
        "purchase amount": "Purchase_Amount", "spending": "Purchase_Amount", "spent": "Purchase_Amount",
        "order value": "Average_Order_Value", "average order": "Average_Order_Value", "aov": "Average_Order_Value",
        "total purchases": "Total_Purchases", "purchase frequency": "Total_Purchases", "frequency": "Total_Purchases",
        "customer value": "Customer_Value_Score", "value score": "Customer_Value_Score",
        "engagement": "Engagement_Score", "loyalty": "Loyalty_Score", "churn risk": "Churn_Risk_Score",
        "age": "Age", "session duration": "Session_Duration", "pages visited": "Pages_Visited",
        "browsing frequency": "Browsing_Frequency", "feedback": "Feedback_Score",
        "support requests": "Support_Request_Frequency", "repeat purchase rate": "Repeat_Purchase_Rate",
    }
    # Longest aliases first so "customer value" is checked before generic terms.
    for alias in sorted(aliases, key=len, reverse=True):
        if alias in q:
            return aliases[alias]
    return None


def _dataset_lookup(question: str, df: pd.DataFrame, summary: pd.DataFrame):
    """Deterministic natural-language Q&A over the actual project data."""
    q = question.lower().strip()

    customer_answer = _customer_lookup(question, df)
    if customer_answer:
        return customer_answer

    # Dataset and model basics.
    if "how many segment" in q or "number of segment" in q or "how many groups" in q:
        return f"CustomerIQ uses {len(summary)} business segments: " + ", ".join(summary.index) + "."
    if "what are the features" in q or "features used" in q or "model features" in q:
        return ("The K-Means model uses seven features: Purchase Amount, Total Purchases, "
                "Average Order Value, Engagement Score, Loyalty Score, Churn Risk Score, and Customer Value Score.")
    if "which algorithm" in q or "algorithm" in q:
        return "CustomerIQ uses K-Means clustering, an unsupervised machine-learning algorithm, with five clusters."
    if "silhouette" in q:
        return "The current Silhouette Score is 0.2000. For clustering, a higher value generally indicates better-defined separation between groups."
    if "davies" in q or "davies-bouldin" in q:
        return "The current Davies-Bouldin Index is 1.4409. Lower values generally indicate better cluster separation and compactness."
    if "calinski" in q or "calinski-harabasz" in q:
        return "The current Calinski-Harabasz Score is 3385.4. Higher values generally indicate stronger separation relative to within-cluster dispersion."
    if "accuracy" in q:
        return ("CustomerIQ is an unsupervised clustering system, so it does not have classification accuracy. "
                "Its clustering quality is evaluated using Silhouette, Davies-Bouldin and Calinski-Harabasz metrics.")

    # Top customer questions. Resolve these before segment-level comparisons.
    if ("customer" in q or "who" in q) and ("highest spending" in q or "spent the most" in q):
        source = df
        row = source.loc[source["Purchase_Amount"].idxmax()]
        return f"{row['Customer_ID']} has the highest purchase amount at ₹{row['Purchase_Amount']:,.2f}."
    if ("customer" in q or "who" in q) and "highest value" in q:
        row = df.loc[df["Customer_Value_Score"].idxmax()]
        return f"{row['Customer_ID']} has the highest customer-value score at {row['Customer_Value_Score']:.1f}/100."
    if ("customer" in q or "who" in q) and ("highest churn" in q or "most at risk" in q):
        row = df.loc[df["Churn_Risk_Score"].idxmax()]
        return f"{row['Customer_ID']} has the highest churn-risk score at {row['Churn_Risk_Score']:.1f}/100."

    segment = _segment_from_question(question, summary)

    # Segment-specific statistics.
    if segment:
        row = summary.loc[segment]
        if "how many" in q or "number of" in q or ("customers" in q and "segment" in q):
            return f"{segment} contains {int(row.customers):,} customers ({row.percentage:.1f}% of the dataset)."
        # Check the explicitly requested metric before generic words such as
        # "risk" that may appear inside the segment name At-Risk.
        if "spending" in q or "spent" in q or "purchase amount" in q:
            return f"{segment} has an average purchase amount of ₹{row.avg_spending:,.0f}."
        if "frequency" in q or "purchases" in q:
            return f"{segment} averages {row.frequency:.1f} purchases per customer."
        if "engagement" in q:
            return f"{segment} has an average engagement score of {row.engagement:.1f}/100."
        if "loyalty" in q:
            return f"{segment} has an average loyalty score of {row.loyalty:.1f}/100."
        if "churn risk" in q or "churn" in q or "risk score" in q:
            return f"{segment} has an average churn-risk score of {row.churn_risk:.1f}/100."
        if "customer value" in q or "value score" in q:
            return f"{segment} has an average customer-value score of {row.customer_value:.1f}/100."
        if "profile" in q or "details" in q or "about" in q:
            return (f"{segment}: {int(row.customers):,} customers, {row.percentage:.1f}% of the dataset, "
                    f"₹{row.avg_spending:,.0f} average spending, {row.frequency:.1f} average purchases, "
                    f"{row.engagement:.1f}/100 engagement, {row.loyalty:.1f}/100 loyalty, "
                    f"{row.churn_risk:.1f}/100 churn risk, and {row.customer_value:.1f}/100 customer value.")

    # Dataset-level customer count after segment-specific queries have had a chance.
    if "how many customer" in q or "total customer" in q or "dataset size" in q or "number of records" in q:
        return f"The finalized dataset contains {len(df):,} customer records."

    # Highest/lowest segment comparisons.
    if "highest" in q or "best" in q or "maximum" in q:
        if "spending" in q:
            s = summary.avg_spending.idxmax(); return f"{s} has the highest average spending at ₹{summary.loc[s, 'avg_spending']:,.0f}."
        if "engagement" in q:
            s = summary.engagement.idxmax(); return f"{s} has the highest average engagement at {summary.loc[s, 'engagement']:.1f}/100."
        if "loyalty" in q:
            s = summary.loyalty.idxmax(); return f"{s} has the highest average loyalty at {summary.loc[s, 'loyalty']:.1f}/100."
        if "churn" in q or "risk" in q:
            s = summary.churn_risk.idxmax(); return f"{s} has the highest average churn risk at {summary.loc[s, 'churn_risk']:.1f}/100."
        if "customer value" in q or "value" in q:
            s = summary.customer_value.idxmax(); return f"{s} has the highest average customer value at {summary.loc[s, 'customer_value']:.1f}/100."
        if "frequency" in q or "purchases" in q:
            s = summary.frequency.idxmax(); return f"{s} has the highest average purchase frequency at {summary.loc[s, 'frequency']:.1f}."

    if "lowest" in q or "least" in q or "minimum" in q:
        if "spending" in q:
            s = summary.avg_spending.idxmin(); return f"{s} has the lowest average spending at ₹{summary.loc[s, 'avg_spending']:,.0f}."
        if "engagement" in q:
            s = summary.engagement.idxmin(); return f"{s} has the lowest average engagement at {summary.loc[s, 'engagement']:.1f}/100."
        if "churn" in q or "risk" in q:
            s = summary.churn_risk.idxmin(); return f"{s} has the lowest average churn risk at {summary.loc[s, 'churn_risk']:.1f}/100."
        if "customer value" in q or "value" in q:
            s = summary.customer_value.idxmin(); return f"{s} has the lowest average customer value at {summary.loc[s, 'customer_value']:.1f}/100."

    # Whole-dataset numeric questions, optionally scoped to a segment.
    column = _column_from_question(question)
    if column and column in df.columns and any(word in q for word in ("average", "avg", "mean")):
        source = df if segment is None else df[df["Segment"] == segment]
        value = pd.to_numeric(source[column], errors="coerce").mean()
        scope = "in the finalized dataset" if segment is None else f"for {segment}"
        return f"The average {_column_label(column)} {scope} is {_fmt_value(column, value)}."

    if column and column in df.columns and any(word in q for word in ("total", "sum")):
        source = df if segment is None else df[df["Segment"] == segment]
        value = pd.to_numeric(source[column], errors="coerce").sum()
        scope = "in the finalized dataset" if segment is None else f"for {segment}"
        return f"The total {_column_label(column)} {scope} is {_fmt_value(column, value)}."

    if "retention" in q or "retain" in q:
        s = summary.churn_risk.idxmax()
        return f"{s} should be the main retention priority because its average churn risk is {summary.loc[s, 'churn_risk']:.1f}/100."
    if "premium" in q and ("valuable" in q or "why" in q):
        s = "Premium / High-Value"
        return f"{s} is valuable because it has an average customer-value score of {summary.loc[s, 'customer_value']:.1f}/100 and average spending of ₹{summary.loc[s, 'avg_spending']:,.0f}."
    if "category" in q or "prefer" in q or "product" in q and "most common" in q:
        source = df if segment is None else df[df["Segment"] == segment]
        if not source.empty and "Product_Category" in source.columns:
            category = source["Product_Category"].value_counts().idxmax()
            scope = "in the finalized dataset" if segment is None else f"among {segment} customers"
            return f"The most common product category {scope} is {category}."

    if "how" in q and "segment" in q or "create segment" in q or "k-means" in q:
        return ("CustomerIQ uses K-Means clustering on seven behavioral and value features. "
                "The features are standardized, the finalized feature weights are applied, five clusters are learned, "
                "and the clusters are mapped to business-friendly segment names from their verified profiles.")

    if "prediction" in q or "predict" in q:
        return ("Customer Prediction accepts Age, Income Level, Annual Purchase Amount / Spending, and Average Order Value. "
                "These inputs are transformed into the same four-dimensional representation used by the prediction layer, "
                "then compared with the learned segment centroids. The closest centroid determines the predicted segment. "
                "The displayed confidence is a distance-based similarity score, not supervised classification probability.")

    if ("data upload" in q or "uploaded dataset" in q or "upload" in q) and any(word in q for word in ("store", "stored", "happen", "save", "separate", "merge", "replace")):
        return ("Uploaded CSV files are stored separately under data/uploads. They are validated and can be analyzed against "
                "the existing finalized K-Means model, but they are not merged into or used to replace the finalized dataset.")

    return None


def _column_label(column: str) -> str:
    return {
        "Purchase_Amount": "purchase amount",
        "Average_Order_Value": "average order value",
        "Total_Purchases": "total purchases",
        "Customer_Value_Score": "customer-value score",
        "Engagement_Score": "engagement score",
        "Loyalty_Score": "loyalty score",
        "Churn_Risk_Score": "churn-risk score",
        "Age": "age",
        "Session_Duration": "session duration",
        "Pages_Visited": "pages visited",
        "Browsing_Frequency": "browsing frequency",
        "Feedback_Score": "feedback score",
        "Support_Request_Frequency": "support-request frequency",
        "Repeat_Purchase_Rate": "repeat-purchase rate",
    }.get(column, column.replace("_", " ").lower())


def _fallback(question: str, df, summary) -> str:
    answer = _dataset_lookup(question, df, summary)
    if answer:
        return answer
    return (
        "I could not verify that answer from the current CustomerIQ dataset or project statistics. "
        "Try asking about a customer ID, a customer field, a segment, spending, purchase frequency, "
        "engagement, loyalty, churn risk, customer value, categories, model metrics, prediction, or data upload."
    )


def _referenced_customer_context(question: str, df) -> str:
    customer_id = _normalize_customer_id(question)
    if not customer_id:
        return ""
    rows = df[df["Customer_ID"].astype(str).str.upper() == customer_id]
    if rows.empty:
        return f"Referenced customer {customer_id} was not found."
    row = rows.iloc[0]
    columns = [
        "Customer_ID", "Age", "Income_Level", "Product_Category", "Purchase_Amount",
        "Total_Purchases", "Average_Order_Value", "Customer_Value_Score",
        "Engagement_Score", "Loyalty_Score", "Churn_Risk_Score", "Segment",
        "Occupation", "Education_Level", "Location", "Gender", "Payment_Method",
    ]
    columns = [c for c in columns if c in row.index]
    return "Referenced customer record: " + ", ".join(f"{c}={row[c]}" for c in columns)


def answer_question(question: str, df, summary) -> tuple[str, bool]:
    """Return (answer, used_llm). Local verified answers always take priority."""
    local_answer = _dataset_lookup(question, df, summary)
    if local_answer:
        return local_answer, False

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback(question, df, summary), False

    try:
        from openai import OpenAI

        context_lines = []
        for segment in summary.index:
            row = summary.loc[segment]
            context_lines.append(
                f"{segment}: customers={int(row.customers)}, avg_spending={row.avg_spending:.2f}, "
                f"frequency={row.frequency:.2f}, engagement={row.engagement:.2f}, "
                f"loyalty={row.loyalty:.2f}, customer_value={row.customer_value:.2f}, churn_risk={row.churn_risk:.2f}."
            )

        context = "\n".join(context_lines) + "\n" + _referenced_customer_context(question, df)
        prompt = (
            "You are CustomerIQ's grounded project assistant. Answer only from the verified "
            "CustomerIQ context supplied below. Do not invent customer values, statistics, "
            "features, or capabilities. If the supplied data cannot verify an answer, say so. "
            "Keep answers concise and easy to understand.\n\nVERIFIED DATA:\n" + context +
            "\n\nQUESTION:\n" + question
        )
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5.6"),
            input=prompt,
        )
        text = getattr(response, "output_text", "").strip()
        if text:
            return text, True
    except Exception:
        pass

    return _fallback(question, df, summary), False
