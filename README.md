# Customer Segmentation

AI-Powered Customer Intelligence

CustomerIQ is a Streamlit-based customer intelligence application that discovers five behavioral customer groups with K-Means, explains the groups with business-friendly statistics, predicts a new customer's closest segment from the four finalized inputs, and provides grounded analytics and AI assistance.

## Run the project

### 1. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Streamlit

```bash
streamlit run app.py
```

Open `http://localhost:8501`.

## Login

The finalized demo credentials remain:

```text
Email: admin123@gmail.com
Password: admin123
```

The password is stored as a SHA-256 hash in the source, and deployment environment variables can override the demo credentials.

For deployment, set:

```text
CUSTOMERIQ_ADMIN_EMAIL
CUSTOMERIQ_ADMIN_PASSWORD_HASH
```

## Page order

1. Customer Prediction
2. Customer Intelligence
3. Customer Segments
4. Customer Explorer
5. Analytics
6. AI Insights
7. AI Assistant
8. Model Insights
9. Data Upload

No Campaign Generator or Docker configuration is included.

## Machine-learning model

The deployed model remains K-Means with **5 clusters and the same 7 original input features**:

- Purchase Amount
- Total Purchases
- Average Order Value
- Engagement Score
- Loyalty Score
- Churn Risk Score
- Customer Value Score

### Model-quality improvement

The seven features are standardized and then given transparent weights before K-Means:

```text
Purchase Amount       1.00
Total Purchases       1.00
Average Order Value   0.25
Engagement Score      1.00
Loyalty Score         1.00
Churn Risk Score      1.00
Customer Value Score  1.50
```

The goal is to reduce the influence of the highly overlapping Average Order Value signal and give the existing Customer Value signal slightly more influence without removing any original feature.

Current metrics on the finalized 11,780-row dataset:

```text
Silhouette Score       0.2000
Davies-Bouldin Index   1.4409
Calinski-Harabasz      3385.4
```

These should be described as clustering-quality metrics, not classification accuracy.

## Customer Prediction

The existing four-field prediction interface is intentionally unchanged:

- Age
- Income Level (displayed only as lakh ranges)
- Annual Purchase Amount / Spending (₹)
- Average Order Value (₹)

Income ranges are mapped from the dataset's categorical income labels for a readable numeric estimate. The warning remains:

```text
NOTE : annual purchase amount is more than the income
```

The prediction compares the new customer's four standardized fields with the learned segment centroids and converts relative distances into an easy-to-read confidence-style score. This is a **centroid similarity estimate**, not a supervised classification probability.

## AI Assistant

The assistant is grounded in the verified dataset and model statistics. It works in two modes:

1. **Offline mode:** deterministic, data-grounded answers with no external API required.
2. **Optional LLM mode:** if `OPENAI_API_KEY` is configured, the assistant sends only the verified CustomerIQ statistics as context to the OpenAI Responses API and instructs the model not to invent statistics.

Optional environment variables:

```text
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.6
```

Without the key, the project remains fully runnable.

## Authentication

The login screen remains the same visually, but the password is no longer kept as plaintext in the authentication logic. The application compares a SHA-256 password hash and supports environment-variable overrides for deployment.

## Persistent database

The application creates a local SQLite database automatically at runtime:

```text
data/customeriq.db
```

It stores:

- Model training/evaluation runs
- Prediction logs
- Uploaded dataset metadata

The database file is ignored by Git so it is not committed accidentally.

For a production PostgreSQL deployment, set:

```text
DATABASE_URL=postgresql://username:password@host:5432/customeriq
```

The project includes the PostgreSQL driver and uses the same persistence layer when that variable is configured.

## Data Upload

Uploaded CSV files are validated for the seven required model features. When they are present, the **already trained finalized K-Means model** is used to assign the uploaded records to the same five business segments. The page shows:

- Rows
- Columns
- Missing values
- Dataset preview
- Segment counts
- Segment percentages
- Segment distribution chart
- Segment profile table

The upload metadata is also persisted in the database.

## Project structure

```text
CustomerIQ/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── data/
│   └── Customer_Segmentation_Dataset.csv
├── pages/
│   ├── 1_Customer_Segments.py
│   ├── 2_Customer_Explorer.py
│   ├── 3_Customer_Prediction.py
│   ├── 4_Analytics.py
│   ├── 5_AI_Insights.py
│   ├── 6_AI_Assistant.py
│   ├── 7_Model_Insights.py
│   └── 8_Data_Upload.py
├── services/
│   ├── auth.py
│   ├── customer_engine.py
│   ├── database.py
│   ├── ai_service.py
│   └── ui.py
└── .streamlit/
    └── config.toml
```

There is no Docker setup, no unused backend, no campaign generator, and no virtual-environment folder in the project archive.
