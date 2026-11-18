# E-Commerce Business Intelligence & Growth Analytics

An end-to-end e-commerce analytics project built using Python, SQL, SQLite and Streamlit to analyse business performance, customer behaviour, product categories and delivery operations.

## Project Overview

This project uses the **Olist Brazilian E-Commerce Public Dataset (2016–2018)** to transform raw transaction data into meaningful business insights.

The objective is to understand sales trends, customer purchasing patterns, product performance and operational efficiency through data analysis, SQL queries and an interactive business intelligence dashboard.

## Dashboard Preview

An interactive Streamlit dashboard provides an overview of key business metrics, sales trends, customer segmentation, product categories and delivery performance.

## Tech Stack

| Technology | Application |
|---|---|
| Python | Data analysis and processing |
| Pandas & NumPy | Data manipulation |
| SQL | Business queries and analysis |
| SQLite | Relational database |
| Matplotlib & Seaborn | Data visualisation |
| Streamlit | Interactive dashboard |
| Jupyter Notebook | Exploratory data analysis |

## Key Business Metrics

| Metric | Result |
|---|---:|
| Total GMV | R$15.42 Million |
| Delivered Orders | 96,478 |
| Repeat Purchase Rate | 3.00% |
| Late Delivery Rate | 8.11% |

*Metrics reflect the current dashboard calculations.*

## Business Analysis

### 1. Sales Performance Analysis
- Monthly GMV and order-volume trends
- Product sales and freight-value analysis
- Monthly business performance

### 2. Customer Analytics
- One-time vs repeat customer segmentation
- Customer spending comparison
- Customer purchase frequency
- Cohort-based retention analysis

### 3. Product Category Analysis
- Top-performing product categories
- Category-wise sales performance
- Order volume and average item price

### 4. Seller Performance Analysis
- Seller-level order performance
- Sales contribution analysis
- Seller geographic distribution

### 5. Delivery Operations Analysis
- Late vs on-time delivery performance
- Delivery delay analysis
- Operational performance metrics

## Project Structure

```text
ecommerce-growth-analytics/
│
├── SQL/
│   ├── 01_monthly_revenue.sql
│   ├── 02_customer_repeat_analysis.sql
│   ├── 03_category_performance.sql
│   ├── 04_seller_performance.sql
│   └── 05_delivery_performance.sql
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│   └── 01_data_understanding.ipynb
│
├── outputs/
│
├── presentation/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run the Dashboard

Clone the repository:

```bash
git clone https://github.com/aditi-astro/ecommerce-growth-analytics.git
cd ecommerce-growth-analytics
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## Dataset

**Olist Brazilian E-Commerce Public Dataset**

Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset contains anonymised historical e-commerce transactions from 2016 to 2018.

## Key Business Insights

### Customer Behaviour
- Repeat customers account for approximately **3.0%** of delivered-order customers.
- Repeat customers generate approximately **5.6% of total revenue**.
- Average customer spending is approximately R$308.53 for repeat customers, compared with R$160.73 for one-time customers.

### Product Performance
- Health & Beauty is the highest-selling product category, generating approximately R$1.23 million in product sales.
- Bed, Bath & Table records the highest number of orders among the leading categories.

### Delivery Operations
- Approximately **8.11% of analysed delivered orders** were delivered late.
- Late deliveries have a lower average review score (2.57) compared with on-time deliveries (4.29).

These findings are descriptive and do not establish causal relationships.

## Important Notes

- This project uses historical public data, not live business transactions.
- GMV includes product prices and freight charges for delivered orders. It should not be interpreted as company profit or net revenue.
- Raw datasets and local database files are excluded from the GitHub repository.
- Results are specific to the dataset and analysis methodology.

## Author

**Aditi Singh**
