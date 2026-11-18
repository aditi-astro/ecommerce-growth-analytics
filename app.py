
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "olist_analytics.db"

st.set_page_config(
    page_title="E-Commerce Business Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("E-Commerce Business Intelligence Dashboard")
st.caption("Business analytics using the Olist Brazilian E-Commerce dataset")

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    monthly = pd.read_sql_query("""
        SELECT
            strftime('%Y-%m', o.order_purchase_timestamp) AS month,
            COUNT(DISTINCT o.order_id) AS total_orders,
            ROUND(SUM(oi.price), 2) AS product_sales,
            ROUND(SUM(oi.price + oi.freight_value), 2) AS total_gmv
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY month
        ORDER BY month
    """, conn)

    categories = pd.read_sql_query("""
        SELECT
            COALESCE(ct.product_category_name_english,
                     p.product_category_name, 'Unknown') AS category,
            ROUND(SUM(oi.price), 2) AS product_sales
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN products p ON oi.product_id = p.product_id
        LEFT JOIN category_translation ct
            ON p.product_category_name = ct.product_category_name
        WHERE o.order_status = 'delivered'
        GROUP BY category
        ORDER BY product_sales DESC
        LIMIT 10
    """, conn)

    customers = pd.read_sql_query("""
        SELECT
            customer_type,
            COUNT(*) AS total_customers
        FROM (
            SELECT
                c.customer_unique_id,
                CASE
                    WHEN COUNT(DISTINCT o.order_id) > 1
                    THEN 'Repeat Customer'
                    ELSE 'One-time Customer'
                END AS customer_type
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.order_status = 'delivered'
            GROUP BY c.customer_unique_id
        )
        GROUP BY customer_type
    """, conn)

    delivery = pd.read_sql_query("""
        SELECT
            CASE
                WHEN julianday(order_delivered_customer_date) >
                     julianday(order_estimated_delivery_date)
                THEN 'Late'
                ELSE 'On Time'
            END AS delivery_status,
            COUNT(*) AS total_orders
        FROM orders
        WHERE order_status = 'delivered'
        AND order_delivered_customer_date IS NOT NULL
        AND order_estimated_delivery_date IS NOT NULL
        GROUP BY delivery_status
    """, conn)

    conn.close()
    return monthly, categories, customers, delivery

try:
    monthly, categories, customers, delivery = load_data()

    total_gmv = monthly["total_gmv"].sum()
    total_orders = monthly["total_orders"].sum()

    repeat_count = customers.loc[
        customers["customer_type"] == "Repeat Customer",
        "total_customers"
    ].sum()

    total_customers = customers["total_customers"].sum()
    repeat_rate = repeat_count / total_customers * 100

    late_orders = delivery.loc[
        delivery["delivery_status"] == "Late",
        "total_orders"
    ].sum()

    delivered_orders = delivery["total_orders"].sum()
    late_rate = late_orders / delivered_orders * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total GMV", f"R$ {total_gmv:,.0f}")
    col2.metric("Delivered Orders", f"{total_orders:,}")
    col3.metric("Repeat Purchase Rate", f"{repeat_rate:.2f}%")
    col4.metric("Late Delivery Rate", f"{late_rate:.2f}%")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Monthly GMV")
        st.line_chart(
            monthly.set_index("month")["total_gmv"]
        )

    with right:
        st.subheader("Monthly Order Volume")
        st.bar_chart(
            monthly.set_index("month")["total_orders"]
        )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Top Product Categories")
        st.bar_chart(
            categories.set_index("category")["product_sales"]
        )

    with right:
        st.subheader("Customer Segmentation")
        st.bar_chart(
            customers.set_index("customer_type")["total_customers"]
        )

    st.divider()

    st.subheader("Delivery Performance")
    st.dataframe(delivery, use_container_width=True)

    st.subheader("Monthly Business Data")
    st.dataframe(monthly, use_container_width=True)

    st.caption(
        "Source: Olist Brazilian E-Commerce public dataset (2016–2018). "
        "GMV includes product prices and freight charges for delivered orders; "
        "it is not company profit or net revenue."
    )

except Exception as error:
    st.error(f"Dashboard could not load: {error}")
    st.info("Check that olist_analytics.db exists in the project root.")
