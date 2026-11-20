# CustomerIQ – AI-Powered Customer Intelligence Platform

**Transforming Customer Data into Meaningful Business Insights**

CustomerIQ is an AI-powered customer intelligence and segmentation platform built using Python, Streamlit, and Machine Learning. It analyzes customer purchasing behavior, identifies five behavioral customer segments using K-Means clustering, predicts the closest segment for new customers, and provides interactive analytics and AI-assisted business insights.

The platform brings customer segmentation, prediction, behavioral analysis, data exploration, and business intelligence together in a single application.

<p align="center">

**Live Demo:** https://customersegmentation05.streamlit.app/

**GitHub Repository:** https://github.com/Venkateshdevarapalle/Customer_Segmentation

</p>

---

## Table of Contents

1. [About the Project](#about-the-project)
2. [Project Objectives](#project-objectives)
3. [Key Features](#key-features)
4. [Customer Segments](#customer-segments)
5. [Machine Learning Methodology](#machine-learning-methodology)
6. [Model Evaluation](#model-evaluation)
7. [Customer Prediction](#customer-prediction)
8. [Application Workflow](#application-workflow)
9. [Technology Stack](#technology-stack)
10. [Project Structure](#project-structure)
11. [Installation and Setup](#installation-and-setup)
12. [Application Pages](#application-pages)
13. [AI Assistant](#ai-assistant)
14. [Authentication and Security](#authentication-and-security)
15. [Database and Data Persistence](#database-and-data-persistence)
16. [Data Upload and Analysis](#data-upload-and-analysis)
17. [Environment Configuration](#environment-configuration)
18. [Important Notes](#important-notes)

---

## About the Project

Businesses collect large amounts of customer information, including purchasing history, spending patterns, engagement levels, loyalty, and customer value. However, understanding these records and converting them into meaningful business decisions can be challenging.

CustomerIQ addresses this problem through machine-learning-based customer segmentation.

Using the K-Means clustering algorithm, the application identifies five behavioral customer groups based on seven numerical features.

The platform provides an integrated environment where users can:

- Understand overall customer behavior.
- Identify high-value and at-risk customers.
- Explore individual customer profiles.
- Discover purchasing and engagement patterns.
- Predict the closest customer segment for new customers.
- Analyze customer segments through interactive dashboards.
- Generate data-grounded business insights.
- Interact with customer data using an AI Assistant.
- Upload additional datasets for segmentation analysis.

The objective is to make customer analytics more accessible and useful for data-driven business decisions.

## Project Objectives

The primary objectives of CustomerIQ are:

1. Analyze customer purchasing and behavioral data.
2. Apply machine learning to discover meaningful customer groups.
3. Understand customer spending, engagement, loyalty, and churn risk.
4. Develop an interactive customer prediction interface.
5. Provide business-oriented dashboards and analytics.
6. Generate insights using verified dataset statistics.
7. Enable natural-language interaction with customer information.
8. Support the validation and analysis of additional customer datasets.

---

## Key Features

### 1. Customer Intelligence Dashboard

Provides an overall understanding of the customer base through important business metrics and interactive visualizations.

Key indicators include:

- Total Customers
- Number of Customer Segments
- Average Customer Value
- Average Spending
- Average Purchase Frequency
- High-Value Customers
- At-Risk Customers
- Average Engagement Score

Additional visualizations include:

- Customer Segment Distribution
- Customer Value vs. Spending
- Segment Performance
- AI Executive Summary
- Recommended Business Priorities

### 2. Customer Segmentation

Uses K-Means clustering to discover five behavioral customer groups.

Users can explore individual segments and understand their:

- Customer count
- Customer percentage
- Average spending
- Purchase frequency
- Customer value
- Churn risk
- Behavioral characteristics
- Preferred categories
- Recommended business actions

### 3. Customer Prediction

Allows users to estimate the closest customer segment using four input fields:

- Age
- Income Level
- Annual Purchase Amount / Spending
- Average Order Value

The application compares the input with the learned customer segment centroids and displays the predicted segment along with a similarity-based confidence-style score.

### 4. Customer Explorer

Allows users to search and explore individual customer records.

Available information includes:

- Customer ID
- Age
- Gender
- Income Level
- Occupation
- Location
- Product Category
- Purchase Amount
- Total Purchases
- Customer Value Score
- Engagement Score
- Loyalty Score
- Churn Risk Score
- Discovered Segment
- Reference information, where available

### 5. Interactive Analytics

Provides visual analysis of:

- Customer Spending
- Customer Value
- Customer Engagement
- Segment Performance
- Product Category Behavior
- Customer Distribution

The visualizations help users understand patterns without requiring advanced technical knowledge.

### 6. AI Insights

Converts verified customer statistics into business-friendly explanations.

It focuses on:

- Customer behavior patterns
- High-value customers
- At-risk customers
- Potential growth opportunities
- Business priorities
- Segment-level observations

### 7. AI Assistant

Enables users to interact with CustomerIQ using natural-language questions.

It supports an offline mode and an optional OpenAI-powered mode.

### 8. Model Insights

Displays technical information about the machine-learning model, including:

- Algorithm
- Number of Clusters
- Input Features
- Model Evaluation Metrics
- Dataset Size
- Model Status
- Cluster Profiles

### 9. Data Upload

Allows users to upload additional CSV datasets, validate their structure, and analyze them using the existing trained K-Means model.

Uploaded records remain separate from the original finalized dataset.

---

## Customer Segments

CustomerIQ identifies five behavioral customer groups.

| Segment | Description |
|---|---|
| At-Risk | Customers exhibiting higher churn risk and requiring retention attention. |
| Budget | Customers generally associated with lower spending behavior. |
| Potential | Customers who may represent opportunities for increased engagement and value. |
| Premium / High-Value | Customers associated with stronger customer value and spending. |
| Regular | Customers demonstrating relatively consistent purchasing behavior. |

Each segment is analyzed using its customer distribution, spending, purchase frequency, engagement, loyalty, and customer value characteristics.

The application also provides segment-specific explanations and recommended business actions.

---

## Machine Learning Methodology

CustomerIQ uses **K-Means Clustering**, an unsupervised machine-learning algorithm.

K-Means groups customers according to similarities in their selected behavioral features.

### Model Configuration

| Parameter | Configuration |
|---|---|
| Algorithm | K-Means |
| Number of Clusters | 5 |
| Input Features | 7 |
| Dataset Size | 11,780 customers |
| Feature Preparation | Standardization and Feature Weighting |

### Features Used

The final segmentation model uses seven numerical features:

1. Purchase Amount
2. Total Purchases
3. Average Order Value
4. Engagement Score
5. Loyalty Score
6. Churn Risk Score
7. Customer Value Score

Customer IDs and reference labels are not used as clustering inputs.

### Data Preprocessing

The model preparation process involves:

1. Selecting the required numerical features.
2. Handling missing values where required.
3. Standardizing numerical features.
4. Applying predefined feature weights.
5. Performing K-Means clustering.
6. Evaluating the resulting clusters.

Standardization ensures that features with different numerical ranges can contribute meaningfully to the clustering process.

### Feature Weighting

The finalized model applies the following feature weights:

| Feature | Weight |
|---|---:|
| Purchase Amount | 1.00 |
| Total Purchases | 1.00 |
| Average Order Value | 0.25 |
| Engagement Score | 1.00 |
| Loyalty Score | 1.00 |
| Churn Risk Score | 1.00 |
| Customer Value Score | 1.50 |

Feature weighting was introduced to reduce the influence of the overlapping Average Order Value signal and give Customer Value Score slightly more influence.

All seven original model features are retained.

---

## Model Evaluation

Since K-Means is an unsupervised learning algorithm, classification accuracy is not an appropriate evaluation metric for this model.

CustomerIQ uses three clustering evaluation metrics.

### Silhouette Score

Measures how closely customers fit within their assigned clusters compared with other clusters.

A higher score generally indicates better-separated clusters.

### Davies-Bouldin Index

Measures the similarity between clusters.

A lower value generally indicates better cluster separation.

### Calinski-Harabasz Score

Measures the relationship between between-cluster separation and within-cluster variation.

A higher value generally indicates better-defined clusters.

### Finalized Model Results

The following results were obtained using the finalized 11,780-row dataset.

| Evaluation Metric | Result |
|---|---:|
| Algorithm | K-Means |
| Number of Clusters | 5 |
| Input Features | 7 |
| Silhouette Score | 0.2000 |
| Davies-Bouldin Index | 1.4409 |
| Calinski-Harabasz Score | 3385.4 |
| Dataset Size | 11,780 |

**Note:** These values represent clustering quality and cluster separation. They should not be interpreted as classification accuracy.

---

## Customer Prediction

Customer Prediction provides an interface for estimating the closest learned customer segment for a new customer.

### Input Parameters

The prediction interface accepts four fields:

1. Age
2. Income Level
3. Annual Purchase Amount / Spending
4. Average Order Value

Income levels are displayed using lakh-based ranges for readability.

### Prediction Process

The application prepares the entered values and compares the resulting customer representation with the learned K-Means centroids.

The prediction process can be summarized as:

```text
New Customer
     |
     v
Enter Four Details
     |
     v
Prepare Input Features
     |
     v
Standardize Input Values
     |
     v
Compare with Learned Centroids
     |
     v
Identify Closest Segment
     |
     v
Display Prediction Result
```

The result includes:

- Predicted customer segment
- Confidence-style similarity score
- Explanation based on centroid distance

**Important:** The prediction interface is a similarity-based estimation feature. Its four input fields are not the same as the seven features used to train the original segmentation model. The displayed score is not a supervised classification probability.

---

## Application Workflow

The overall CustomerIQ workflow is:

```text
Customer Dataset
       |
       v
Data Validation
       |
       v
Data Preprocessing
       |
       v
Feature Selection
       |
       v
Feature Standardization
       |
       v
Feature Weighting
       |
       v
K-Means Clustering
       |
       v
Five Customer Segments
       |
       v
Customer Intelligence
       |
       v
Analytics and Customer Explorer
       |
       v
Prediction and AI Insights
       |
       v
AI Assistant
       |
       v
Business Understanding
```

---

## Technology Stack

The project uses Python-based data science, machine learning, visualization, and application development technologies.

| Technology | Purpose |
|---|---|
| Python | Core programming language and application logic |
| Streamlit | Interactive web application and dashboards |
| Pandas | Data processing and manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning and clustering evaluation |
| Plotly | Interactive charts and visualizations |
| SQLite | Local database and persistence |
| PostgreSQL | Optional production database |
| OpenAI API | Optional LLM-powered AI Assistant |
| Git and GitHub | Version control and source-code management |

### Python

Used for application development, data processing, machine learning, and backend logic.

### Streamlit

Used to create the interactive multi-page application, dashboards, forms, charts, and file-upload interfaces.

### Pandas and NumPy

Used for data cleaning, transformation, aggregation, numerical processing, and feature preparation.

### Scikit-learn

Provides the machine-learning components, including:

- KMeans
- StandardScaler
- Silhouette Score
- Davies-Bouldin Index
- Calinski-Harabasz Score

### Plotly

Used to create interactive charts and visualizations for customer analytics.

### SQLite and PostgreSQL

Used for storing model runs, prediction logs, and uploaded dataset metadata.

### OpenAI API

Provides optional language-model functionality for the AI Assistant.

---

## Project Structure

```text
Customer_Segmentation/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── Customer_Segmentation_Dataset.csv
│   └── uploads/
│
├── pages/
│   ├── 1_Customer_Segments.py
│   ├── 2_Customer_Explorer.py
│   ├── 3_Customer_Prediction.py
│   ├── 4_Analytics.py
│   ├── 5_AI_Insights.py
│   ├── 6_AI_Assistant.py
│   ├── 7_Model_Insights.py
│   └── 8_Data_Upload.py
│
└── services/
    ├── auth.py
    ├── customer_engine.py
    ├── database.py
    ├── ai_service.py
    └── ui.py
```

The application also creates its SQLite database at runtime when local persistence is used.

---

## Installation and Setup

Follow these steps to run CustomerIQ locally.

### Prerequisites

- Python 3.10 or later (use a version compatible with the installed dependencies).
- Git
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/Venkateshdevarapalle/Customer_Segmentation.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Customer_Segmentation
```

### Step 3: Create a Virtual Environment

**Windows:**

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

### Step 6: Open the Application

Visit:

```text
http://localhost:8501
```

The CustomerIQ application will open in your browser.

---

## Application Pages

CustomerIQ contains nine main application pages.

| No. | Page | Purpose |
|---:|---|---|
| 1 | Customer Prediction | Estimate the closest segment for new customers. |
| 2 | Customer Intelligence | View overall customer intelligence and business metrics. |
| 3 | Customer Segments | Explore the five discovered behavioral groups. |
| 4 | Customer Explorer | Search and inspect individual customer profiles. |
| 5 | Analytics | Visualize customer spending and behavioral patterns. |
| 6 | AI Insights | Understand data-grounded business insights. |
| 7 | AI Assistant | Ask natural-language questions about the project and dataset. |
| 8 | Model Insights | Review model configuration and evaluation metrics. |
| 9 | Data Upload | Validate and analyze additional customer datasets. |

---

## AI Assistant

The CustomerIQ AI Assistant allows users to ask questions about customer information, machine-learning results, and business statistics using natural language.

### Example Questions

- How many customers are there?
- What is the average spending?
- What is the average customer value?
- Tell me about CUST_00001.
- What is the age of CUST_00045?
- Which segment has the highest customer value?
- How many customers are in the Premium segment?
- What is the average churn risk?
- Which features are used by the model?
- What is the Silhouette Score?
- How does K-Means create customer segments?
- How does Customer Prediction work?

### Operating Modes

**1. Offline Mode**

- Works without an external AI API.
- Provides deterministic answers to supported questions.
- Uses verified dataset information and calculated project statistics.
- Does not require an OpenAI API key.

**2. Optional LLM Mode**

When an OpenAI API key is configured, the application can use the OpenAI Responses API to generate more natural-language answers.

Only verified CustomerIQ statistics are supplied as context, with instructions to avoid inventing numerical information.

The project remains runnable without the API key.

---

## Authentication and Security

CustomerIQ includes a login system to control access to the application.

The authentication implementation:

- Uses SHA-256 password hashing instead of keeping the password as plaintext in authentication logic.
- Supports environment-variable overrides for deployment.
- Provides demo credentials for testing.

### Demo Login Credentials

```text
Email: admin123@gmail.com
Password: admin123
```

**Security recommendation:** These are demo credentials only. Configure a unique password hash and appropriate secrets for any public or production deployment. Never expose private credentials or API keys in the repository.

---

## Database and Data Persistence

CustomerIQ uses SQLite for local database persistence.

The database is automatically created at runtime:

```text
data/customeriq.db
```

### Stored Information

- Model training and evaluation runs
- Customer prediction logs
- Uploaded dataset metadata

The SQLite database is excluded from Git using `.gitignore` to prevent accidental commits of runtime data.

### Optional PostgreSQL Configuration

The application also supports PostgreSQL when the database connection variable is configured.

Set:

```text
DATABASE_URL=postgresql://username:password@host:5432/customeriq
```

The project includes the PostgreSQL driver and uses the configured persistence layer when this variable is available.

---

## Data Upload and Analysis

The Data Upload page allows users to analyze additional customer datasets without modifying the original finalized dataset.

### Validation

Uploaded CSV files are checked for:

- Number of rows
- Number of columns
- Missing values
- Required model features
- Dataset preview

### Segmentation

When the required seven model features are available, the application uses the already-trained finalized K-Means model to assign uploaded records to the existing five customer segments.

### Analysis Results

The application displays:

- Segment counts
- Segment percentages
- Segment distribution chart
- Segment profile table
- Dataset information

Uploaded dataset metadata is also stored in the database.

**Important:** Uploaded datasets are analyzed separately. They do not automatically replace or merge with the original finalized dataset, and the upload process does not imply that the model is retrained.

---

## Environment Configuration

CustomerIQ supports optional environment variables for deployment and additional functionality.

### Available Variables

| Variable | Purpose |
|---|---|
| `CUSTOMERIQ_ADMIN_EMAIL` | Overrides the demo administrator email. |
| `CUSTOMERIQ_ADMIN_PASSWORD_HASH` | Sets the administrator password hash. |
| `DATABASE_URL` | Configures an optional PostgreSQL database. |
| `OPENAI_API_KEY` | Enables optional OpenAI-powered responses. |
| `OPENAI_MODEL` | Specifies the OpenAI model to use. |

### OpenAI Configuration

For optional LLM functionality:

```text
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-5.6
```

Without an API key, the application continues to operate in offline mode.

Refer to `.env.example` for the project's environment configuration template.

Never commit actual API keys, database passwords, or private credentials.

---

## Important Notes

- The finalized segmentation model uses five K-Means clusters.
- Seven original behavioral features are used for clustering.
- Customer Prediction uses a separate four-field input interface.
- The prediction confidence-style score represents centroid similarity, not classification probability.
- Clustering metrics are not classification accuracy.
- Uploaded datasets are processed separately from the original dataset.
- The AI Assistant supports offline operation.
- OpenAI integration is optional.
- Runtime databases and uploaded customer files should not be committed to GitHub.
- The project does not include a Campaign Generator or Docker configuration.

---

## Author

**Devarapalle Venkatesh**

Computer Science and Data Science

GitHub: https://github.com/Venkateshdevarapalle

---

## Project

**CustomerIQ – AI-Powered Customer Intelligence Platform**

*Turning customer data into meaningful insights for smarter business decisions.*
