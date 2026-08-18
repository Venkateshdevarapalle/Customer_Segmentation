from pathlib import Path
from functools import lru_cache

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

from services.database import initialize_database, save_model_run, log_prediction

BASE = Path(__file__).resolve().parents[1]
DATA_PATH = BASE / "data" / "Customer_Segmentation_Dataset.csv"

SEGMENT_ORDER = ["At-Risk", "Budget", "Potential", "Premium / High-Value", "Regular"]
SEGMENT_COLORS = {
    "At-Risk": "#FEE2E2",
    "Budget": "#FEF3C7",
    "Potential": "#DBEAFE",
    "Premium / High-Value": "#EDE9FE",
    "Regular": "#DCFCE7",
}
SEGMENT_COLORS_HEX = {
    "At-Risk": "#EF4444",
    "Budget": "#F59E0B",
    "Potential": "#06B6D4",
    "Premium / High-Value": "#6366F1",
    "Regular": "#22C55E",
}
SEGMENT_BORDERS = SEGMENT_COLORS_HEX.copy()
SEGMENT_DESCRIPTIONS = {
    "At-Risk": "Customers showing weaker engagement or loyalty signals and comparatively elevated churn risk.",
    "Budget": "Price-conscious customers with lower spending/value signals and room to grow.",
    "Potential": "Customers with encouraging engagement or loyalty signals who can be developed into higher-value customers.",
    "Premium / High-Value": "Customers with strong value and purchasing signals who are important to retain.",
    "Regular": "Customers with balanced, consistent behavior across the main business indicators.",
}

# All seven original model inputs are retained. Feature weights reduce the influence of
# the highly overlapping Average Order Value signal and give Customer Value a little more
# influence. This keeps the model interpretable while improving cluster separation.
MODEL_FEATURES = [
    "Purchase_Amount", "Total_Purchases", "Average_Order_Value",
    "Engagement_Score", "Loyalty_Score", "Churn_Risk_Score", "Customer_Value_Score"
]
MODEL_FEATURE_WEIGHTS = np.array([1.0, 1.0, 0.25, 1.0, 1.0, 1.0, 1.5])
MODEL_VERSION = "v1.1-weighted-kmeans"
PREDICT_FEATURES = ["Age", "Income_Value_Lakh", "Purchase_Amount", "Average_Order_Value"]
INCOME_RANGES = {
    "Low": (2.0, 4.0),
    "Lower Middle": (4.0, 6.0),
    "Middle": (6.0, 10.0),
    "Upper Middle": (10.0, 15.0),
    "High": (15.0, 25.0),
}


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Income_Value_Lakh"] = df["Income_Level"].map(
        lambda x: np.mean(INCOME_RANGES.get(x, (6.0, 10.0)))
    )
    return df


def _label_clusters(df, raw_labels):
    temp = df.copy()
    temp["_cluster"] = raw_labels
    profiles = temp.groupby("_cluster").agg(
        spending=("Purchase_Amount", "mean"),
        frequency=("Total_Purchases", "mean"),
        value=("Customer_Value_Score", "mean"),
        engagement=("Engagement_Score", "mean"),
        loyalty=("Loyalty_Score", "mean"),
        churn=("Churn_Risk_Score", "mean"),
        count=("Customer_ID", "count"),
    )
    score = profiles.copy()
    score["high_value"] = score["value"].rank(pct=True) + score["spending"].rank(pct=True)
    premium = score["high_value"].idxmax()
    # Prioritize elevated churn first, then weaker engagement/loyalty signals.
    at_risk = (
        2.0 * score["churn"].rank(pct=True)
        + 1.0 * (1.0 - score["engagement"].rank(pct=True))
        + 0.75 * (1.0 - score["loyalty"].rank(pct=True))
    ).idxmax()
    remaining = [i for i in profiles.index if i not in {premium, at_risk}]
    budget = min(remaining, key=lambda i: profiles.loc[i, "spending"] + profiles.loc[i, "value"] * 100)
    remaining = [i for i in remaining if i != budget]
    potential = max(
        remaining,
        key=lambda i: profiles.loc[i, "engagement"] + profiles.loc[i, "loyalty"] - profiles.loc[i, "churn"],
    )
    regular = [i for i in remaining if i != potential][0]
    mapping = {
        at_risk: "At-Risk",
        budget: "Budget",
        potential: "Potential",
        premium: "Premium / High-Value",
        regular: "Regular",
    }
    return mapping, profiles


@lru_cache(maxsize=1)
def build_model():
    initialize_database()
    df = load_data()
    X = df[MODEL_FEATURES].fillna(df[MODEL_FEATURES].median())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_weighted = X_scaled * MODEL_FEATURE_WEIGHTS

    model = KMeans(n_clusters=5, random_state=42, n_init=20)
    labels = model.fit_predict(X_weighted)
    mapping, profiles = _label_clusters(df, labels)
    df["Cluster"] = labels
    df["Segment"] = pd.Series(labels, index=df.index).map(mapping)

    metrics = {
        "silhouette": float(silhouette_score(X_weighted, labels)),
        "davies_bouldin": float(davies_bouldin_score(X_weighted, labels)),
        "calinski_harabasz": float(calinski_harabasz_score(X_weighted, labels)),
    }
    # Prediction remains a transparent four-input centroid estimator. The user-facing
    # prediction fields are intentionally not changed from the finalized project.
    pred_centroids = df.groupby("Segment")[PREDICT_FEATURES].mean().reindex(SEGMENT_ORDER)
    pred_scaler = StandardScaler()
    pred_scaled = pred_scaler.fit_transform(pred_centroids)

    save_model_run(metrics, features=len(MODEL_FEATURES), clusters=5, version=MODEL_VERSION)
    return df, model, scaler, mapping, metrics, pred_centroids, pred_scaler, pred_scaled


def get_model_data():
    return build_model()


def segment_summary(df):
    out = df.groupby("Segment").agg(
        customers=("Customer_ID", "count"),
        avg_spending=("Purchase_Amount", "mean"),
        frequency=("Total_Purchases", "mean"),
        engagement=("Engagement_Score", "mean"),
        customer_value=("Customer_Value_Score", "mean"),
        churn_risk=("Churn_Risk_Score", "mean"),
    ).reindex(SEGMENT_ORDER)
    out["percentage"] = out["customers"] / len(df) * 100
    return out


def predict_segment(age, income_lakh, spending, aov):
    _, _, _, _, _, pred_centroids, pred_scaler, pred_scaled = build_model()
    row = pd.DataFrame([[age, income_lakh, spending, aov]], columns=PREDICT_FEATURES)
    row_scaled = pred_scaler.transform(row)
    distances = np.linalg.norm(pred_scaled - row_scaled[0], axis=1)
    temperature = max(float(np.std(distances)), 0.05)
    weights = np.exp(-(distances - distances.min()) / temperature)
    probabilities = weights / weights.sum()
    labels = list(pred_centroids.index)
    idx = int(np.argmax(probabilities))
    segment = labels[idx]
    confidence = float(probabilities[idx])
    probability_map = dict(zip(labels, probabilities * 100))
    log_prediction(age, income_lakh, spending, aov, segment, confidence)
    return segment, confidence, pred_centroids, probability_map


def customer_profile(df, customer_id):
    rows = df[df["Customer_ID"].astype(str) == str(customer_id)]
    return rows.iloc[0] if not rows.empty else None


def category_counts(df, segment=None):
    source = df if segment in (None, "All") else df[df["Segment"] == segment]
    return source["Product_Category"].value_counts().sort_values(ascending=False)
