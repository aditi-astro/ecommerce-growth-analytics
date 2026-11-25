
import streamlit as st
import pandas as pd
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"

# Page configuration
st.set_page_config(
    page_title="E-Commerce Business Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("E-Commerce Business Intelligence Dashboard")
st.caption(
    "Business analytics using the Olist Brazilian E-Commerce dataset (2016–2018)"
)


# Load CSV files
@st.cache_data
def load_data():
    customer = pd.read_csv(OUTPUTS / "customer_summary.csv")
    monthly = pd.read_csv(OUTPUTS / "monthly_revenue.csv")
    categories = pd.read_csv(OUTPUTS / "sql_category_analysis.csv")
    delivery = pd.read_csv(OUTPUTS / "sql_delivery_analysis.csv")

    return customer, monthly, categories, delivery


try:
    customer, monthly, categories, delivery = load_data()

    # -------------------------------
    # KPI SECTION
    # -------------------------------
    st.header("Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Customer Records", f"{len(customer):,}")
    col2.metric("Monthly Records", f"{len(monthly):,}")
    col3.metric("Product Categories", f"{len(categories):,}")
    col4.metric("Delivery Records", f"{len(delivery):,}")

    st.divider()

    # -------------------------------
    # MONTHLY REVENUE
    # -------------------------------
    st.header("📈 Monthly Revenue Analysis")

    st.write(
        "Monthly business performance based on delivered orders. "
        "GMV includes product prices and freight charges; "
        "it is not company profit."
    )

    st.dataframe(monthly, use_container_width=True)

    # Find suitable numeric columns for plotting
    numeric_monthly = monthly.select_dtypes(include="number")

    if not numeric_monthly.empty:
        st.subheader("Monthly Revenue Trend")

        revenue_candidates = [
            col for col in numeric_monthly.columns
            if "gmv" in col.lower()
            or "revenue" in col.lower()
            or "sales" in col.lower()
        ]

        if revenue_candidates:
            revenue_col = revenue_candidates[0]
            st.line_chart(monthly.set_index(monthly.columns[0])[revenue_col])
        else:
            st.bar_chart(numeric_monthly)

    st.divider()

    # -------------------------------
    # CATEGORY PERFORMANCE
    # -------------------------------
    st.header("🛍️ Product Category Performance")

    st.dataframe(categories, use_container_width=True)

    category_candidates = [
        col for col in categories.columns
        if "category" in col.lower()
        or "product" in col.lower()
    ]

    sales_candidates = [
        col for col in categories.columns
        if "sales" in col.lower()
        or "revenue" in col.lower()
        or "gmv" in col.lower()
    ]

    if category_candidates and sales_candidates:
        category_col = category_candidates[0]
        sales_col = sales_candidates[0]

        category_plot = categories[
            [category_col, sales_col]
        ].dropna()

        category_plot = category_plot.sort_values(
            sales_col, ascending=False
        ).head(10)

        st.subheader("Top 10 Categories by Sales")

        st.bar_chart(
            category_plot.set_index(category_col)[sales_col]
        )

    st.divider()

    # -------------------------------
    # CUSTOMER ANALYSIS
    # -------------------------------
    st.header("👥 Customer Behaviour")

    st.dataframe(customer, use_container_width=True)

    customer_candidates = [
        col for col in customer.columns
        if "customer_type" in col.lower()
        or "segment" in col.lower()
        or "customer_segment" in col.lower()
    ]

    count_candidates = [
        col for col in customer.columns
        if "customer" in col.lower()
        and ("count" in col.lower() or "total" in col.lower())
    ]

    if customer_candidates and count_candidates:
        segment_col = customer_candidates[0]
        count_col = count_candidates[0]

        st.subheader("Customer Segmentation")

        st.bar_chart(
            customer.set_index(segment_col)[count_col]
        )

    st.divider()

    # -------------------------------
    # DELIVERY PERFORMANCE
    # -------------------------------
    st.header("🚚 Delivery Performance")

    st.dataframe(delivery, use_container_width=True)

    delivery_candidates = [
        col for col in delivery.columns
        if "status" in col.lower()
        or "delivery_type" in col.lower()
        or "performance" in col.lower()
    ]

    delivery_count_candidates = [
        col for col in delivery.columns
        if "count" in col.lower()
        or "orders" in col.lower()
    ]

    if delivery_candidates and delivery_count_candidates:
        status_col = delivery_candidates[0]
        count_col = delivery_count_candidates[0]

        st.subheader("Delivery Status")

        st.bar_chart(
            delivery.set_index(status_col)[count_col]
        )

    st.divider()

    # -------------------------------
    # DATA SOURCE
    # -------------------------------
    st.subheader("About the Dataset")

    st.markdown(
        """
        - **Dataset:** Olist Brazilian E-Commerce
        - **Period:** 2016–2018
        - **Tools:** Python, Pandas, SQL, SQLite and Streamlit
        - **Analysis:** Revenue, customer behaviour, category performance
          and delivery operations
        """
    )

    st.caption(
        "This dashboard analyses historical, anonymised public dataset "
        "records and does not represent current company performance."
    )

except FileNotFoundError as error:
    st.error("A required CSV file could not be found.")
    st.write(error)
    st.info(
        "Please check that all four CSV files are present "
        "inside the repository's outputs folder."
    )

except Exception as error:
    st.error("Dashboard encountered an error.")
    st.write(error)
