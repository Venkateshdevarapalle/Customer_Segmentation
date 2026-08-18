# Customer Segmentation

### AI-Powered Customer Intelligence

Customer Segmentation is a customer intelligence application built with Python and Streamlit. It uses K-Means clustering to group customers based on their spending, purchase behavior, engagement, loyalty, churn risk and customer value.

The application helps users understand different types of customers, explore individual customer profiles, analyze business patterns, predict the closest segment for a new customer and get data-based insights through an AI Assistant.

Live Demo: https://customersegmentation05.streamlit.app/

GitHub: https://github.com/Venkateshdevarapalle/Customer_Segmentation


## About the Project

Businesses collect a large amount of customer data, but it is not always easy to understand what that data means from a business point of view.

Customer Segmentation converts the available customer data into five behavioral groups using K-Means clustering.

The five groups identified in the project are:

- At-Risk
- Budget
- Potential
- Premium / High-Value
- Regular

The application then provides dashboards, customer profiles, analytics, segment details, prediction, AI insights and model information in one place.


## What the Project Does

The project mainly focuses on the following:

- Analyze customer data
- Prepare the data for machine learning
- Discover customer segments using K-Means
- Understand the behavior of each segment
- Explore individual customers
- Predict the closest segment for a new customer
- Analyze spending, engagement and customer value
- Generate business-oriented insights
- Answer questions about the dataset through an AI Assistant
- Upload and analyze another customer dataset without changing the original dataset


## Main Features


### Customer Prediction

This is the main user-facing prediction feature of the project.

A user enters:

- Age
- Income Level
- Annual Purchase Amount / Spending
- Average Order Value

The application then estimates which of the five learned customer segments the new customer is closest to.

The result shows:

- Predicted segment
- Confidence-style score
- Explanation based on the distance from the learned K-Means centroids

The displayed confidence is a similarity estimate based on cluster distance. It is not the probability of a supervised classification model.


### Customer Intelligence

Customer Intelligence provides an overall view of the customer base.

The page shows important numbers such as:

- Total Customers
- Customer Segments
- Average Customer Value
- Average Spending
- Average Purchase Frequency
- High-Value Customers
- At-Risk Customers
- Average Engagement Score

It also includes:

- Customer Segment Distribution
- Customer Value vs. Spending
- Segment Performance
- AI Executive Summary
- Recommended Business Priorities

The purpose of this page is to give a quick business-level understanding of the complete customer base.


### Customer Segments

This page explains the five groups discovered by the K-Means model.

For each segment, the application displays:

- Number of customers
- Percentage of customers
- Average spending
- Purchase frequency
- Customer value
- Churn risk
- Segment description

A user can select a segment and view more details about that particular group.

The segment detail section includes:

- Customer statistics
- Behavioral profile
- Preferred categories
- Customer value distribution
- Business explanation
- Recommended action


### Customer Explorer

Customer Explorer is used to look at individual customers.

Users can search and select a customer to see details such as:

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
- Reference information where available

This makes it easier to understand the behavior of a particular customer instead of looking only at overall statistics.


### Analytics

The Analytics page provides simple visualizations for understanding customer behavior.

The main areas covered are:

- Spending
- Customer Value
- Engagement
- Segment Performance
- Category Behavior
- Customer Distribution

The charts are kept simple so that both technical and non-technical users can understand them easily.


### AI Insights

AI Insights converts verified customer and segment statistics into business-friendly explanations.

It focuses on areas such as:

- Customer behavior patterns
- High-value customers
- At-risk customers
- Potential growth opportunities
- Recommended business priorities

The insights are based on the statistics calculated from the dataset and the segmentation model.


### AI Assistant

The AI Assistant allows users to ask questions about the Customer Segmentation project and its data using normal language.

For example:

- How many customers are there?
- What is the average spending?
- What is the age of CUST_00045?
- Tell me about CUST_00001.
- Which segment has the highest customer value?
- How many customers are in the Premium segment?
- What is the average churn risk?
- What features are used by the model?
- What is the Silhouette Score?
- How does K-Means create the segments?
- How does Customer Prediction work?

The assistant has two possible modes.

Offline mode:

The application can answer supported questions directly from the verified dataset and calculated project statistics. This mode does not require an external AI API.

Optional LLM mode:

If an OpenAI API key is configured, the assistant can use an external language model to provide more natural responses. The verified Customer Segmentation statistics are provided as context so that the model can answer based on the project data instead of making up statistics.

The AI Assistant is designed specifically around this project and its customer data.


### Model Insights

Model Insights provides the technical details of the K-Means model.

It includes:

- Algorithm
- Number of Clusters
- Features Used
- Silhouette Score
- Davies-Bouldin Index
- Calinski-Harabasz Score
- Dataset Size
- Model Status
- Evaluation Metrics
- Cluster Profiles

This page is mainly useful for understanding how the machine-learning model was built and how well the discovered clusters are separated.


### Data Upload

The Data Upload page allows another CSV file to be uploaded for validation and analysis.

The uploaded file is kept separate from the finalized dataset.

The application checks:

- Number of rows
- Number of columns
- Missing values
- Required model features
- Dataset preview

If the required model fields are available, the existing trained K-Means model can be used to assign the uploaded records to the existing five segments.

The page can then show:

- Segment counts
- Segment percentages
- Segment distribution
- Segment profiles

The uploaded data does not automatically replace or merge with the original finalized dataset.


## Machine Learning

The project uses K-Means clustering.

K-Means is an unsupervised machine-learning algorithm. It groups customers based on similarities in their selected behavioral features.

The final model uses:

- 5 clusters
- 7 input features


### Features Used

The seven model features are:

1. Purchase Amount
2. Total Purchases
3. Average Order Value
4. Engagement Score
5. Loyalty Score
6. Churn Risk Score
7. Customer Value Score

Customer IDs and reference labels are not used as clustering inputs.


## Data Processing

Before sending the data to K-Means, the selected numerical features are prepared for the model.

The main steps are:

1. Select the required model features
2. Handle missing values where required
3. Standardize the numerical features
4. Apply the defined feature weights
5. Run K-Means clustering

Standardization is important because the features have different ranges.

For example, Purchase Amount can have values in thousands, while Engagement Score is measured on a 0–100 scale.

Without standardization, a feature with larger numerical values could have too much influence on the clustering result.


## Feature Weights

The final model uses the following weights:

| Feature | Weight |
|---|---:|
| Purchase Amount | 1.00 |
| Total Purchases | 1.00 |
| Average Order Value | 0.25 |
| Engagement Score | 1.00 |
| Loyalty Score | 1.00 |
| Churn Risk Score | 1.00 |
| Customer Value Score | 1.50 |

The weights were introduced to reduce the influence of the overlapping Average Order Value feature and give slightly more importance to Customer Value Score.

All seven original features are still retained in the model.


## Model Evaluation

Since K-Means is an unsupervised learning algorithm, normal classification accuracy is not used to evaluate the segmentation model.

Instead, the project uses clustering evaluation metrics.

### Silhouette Score

The Silhouette Score indicates how well customers fit within their assigned cluster compared with other clusters.

A higher value generally indicates better-separated clusters.

### Davies-Bouldin Index

The Davies-Bouldin Index measures the similarity between the different clusters.

A lower value generally indicates better cluster separation.

### Calinski-Harabasz Score

The Calinski-Harabasz Score compares the separation between clusters with the variation within each cluster.

A higher value generally indicates better-defined clusters.

### Current Model Results

The current model results on the finalized dataset are:

| Metric | Result |
|---|---:|
| Algorithm | K-Means |
| Number of Clusters | 5 |
| Features | 7 |
| Silhouette Score | 0.2000 |
| Davies-Bouldin Index | 1.4409 |
| Calinski-Harabasz Score | 3385.4 |
| Dataset Size | 11,780 customers |

These values describe clustering quality. They should not be referred to as classification accuracy.


## How Customer Prediction Works

The prediction page asks for four values:

- Age
- Income Level
- Annual Purchase Amount / Spending
- Average Order Value

The application prepares these values and compares the new customer's characteristics with the learned behavioral groups.

The basic flow is:

New Customer

↓

Enter four details

↓

Prepare the input

↓

Standardize the values

↓

Compare with learned K-Means centroids

↓

Find the closest segment

↓

Display the predicted segment


The prediction is therefore based on similarity to the existing customer groups.

It is important to note that the prediction page is a user-friendly estimation feature. The main K-Means segmentation model itself was trained using seven behavioral features.


## Application Flow

The overall working of the project can be understood as:

Customer Dataset

↓

Data Validation

↓

Data Preprocessing

↓

Feature Preparation

↓

Feature Standardization

↓

K-Means Clustering

↓

Five Customer Segments

↓

Customer Intelligence & Analytics

↓

Customer Explorer / Prediction / AI Insights

↓

AI Assistant

↓

Business Understanding and Decisions


## Technologies Used

### Python

Python is used throughout the project for data processing, machine learning, application logic and AI-related functionality.

It was selected because it provides a strong ecosystem for data science and machine learning and allows the complete project to be developed using one main programming language.


### Streamlit

Streamlit is used to build the web application.

It provides the UI components, multi-page navigation, forms, tables, charts, file upload functionality and deployment support required by the project.

Using Streamlit also allows the data-science and application layers to stay within the Python ecosystem.


### Pandas

Pandas is used for:

- Reading CSV files
- Data cleaning
- Data filtering
- Data transformation
- Grouping and aggregation
- Customer analysis


### NumPy

NumPy is used for numerical operations and preparing data for the machine-learning pipeline.


### Scikit-learn

Scikit-learn is used for the machine-learning part of the project.

It provides:

- KMeans
- StandardScaler
- Silhouette Score
- Davies-Bouldin Index
- Calinski-Harabasz Score


### Plotly

Plotly is used to create the interactive charts and graphs used throughout the application.


### SQLite

SQLite is used for lightweight local data persistence.

The application can store information such as:

- Model training and evaluation runs
- Prediction logs
- Uploaded dataset metadata

The SQLite database is created during runtime and is not committed to GitHub.


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
│   └── Customer_Segmentation_Dataset.csv
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
