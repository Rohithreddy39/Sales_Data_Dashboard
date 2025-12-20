"""
Streamlit Dashboard - Interactive Sales Analysis
Run with: streamlit run src/dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Import our modules
import sys
sys.path.append('.')
from data_generator import generate_sales_data
from data_processor import process_sales_data
from analyzer import SalesAnalyzer


# --- Page Configuration ---
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- Data Loading ---
@st.cache_data
def load_data(num_records=1000):
    """Generate and cache sales data."""
    raw = generate_sales_data(num_records)
    df = process_sales_data(raw)
    return df


# --- Sidebar ---
st.sidebar.title("📊 Sales Dashboard")
st.sidebar.markdown("---")

# Data controls
st.sidebar.subheader("Data Settings")
num_records = st.sidebar.slider("Number of Records", 100, 5000, 1000, 100)

# Filters
st.sidebar.subheader("Filters")

# Load data
df = load_data(num_records)

# Category filter
categories = ['All'] + list(df['category'].unique())
selected_category = st.sidebar.selectbox("Category", categories)

# Region filter
regions = ['All'] + list(df['region'].unique())
selected_region = st.sidebar.selectbox("Region", regions)

# Date range filter
min_date = df['date'].min().date()
max_date = df['date'].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters
filtered_df = df.copy()
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['region'] == selected_region]
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['date'].dt.date >= date_range[0]) & 
        (filtered_df['date'].dt.date <= date_range[1])
    ]

# --- Main Content ---
st.title("📈 Sales Analytics Dashboard")
st.markdown("Interactive analysis of sales data using NumPy, Pandas, and Streamlit")

# --- KPI Metrics ---
st.markdown("### Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = filtered_df['revenue'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.0f}")

with col2:
    total_transactions = len(filtered_df)
    st.metric("Transactions", f"{total_transactions:,}")

with col3:
    avg_order = filtered_df['revenue'].mean()
    st.metric("Avg Order Value", f"${avg_order:.2f}")

with col4:
    total_units = filtered_df['quantity'].sum()
    st.metric("Units Sold", f"{total_units:,}")

st.markdown("---")

# --- Charts Row 1 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Category")
    category_rev = filtered_df.groupby('category', observed=True)['revenue'].sum().sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(category_rev.index, category_rev.values, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
    ax.set_xlabel('Revenue ($)')
    for bar, value in zip(bars, category_rev.values):
        ax.text(value + 500, bar.get_y() + bar.get_height()/2, f'${value:,.0f}', va='center', fontsize=9)
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("Revenue by Region")
    region_rev = filtered_df.groupby('region', observed=True)['revenue'].sum()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(region_rev.values, labels=region_rev.index, autopct='%1.1f%%',
           colors=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
    ax.set_title('')
    st.pyplot(fig)
    plt.close()

# --- Charts Row 2 ---
st.subheader("Monthly Revenue Trend")

monthly = filtered_df.groupby(filtered_df['date'].dt.to_period('M')).agg({
    'revenue': 'sum',
    'quantity': 'sum'
}).reset_index()
monthly['date'] = monthly['date'].astype(str)

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(monthly['date'], monthly['revenue'], alpha=0.3, color='#3498db')
ax.plot(monthly['date'], monthly['revenue'], marker='o', linewidth=2, color='#3498db')
ax.set_xlabel('Month')
ax.set_ylabel('Revenue ($)')
plt.xticks(rotation=45)
st.pyplot(fig)
plt.close()

# --- Charts Row 3 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=filtered_df, x='revenue', kde=True, ax=ax, color='#3498db')
    ax.set_xlabel('Revenue ($)')
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("Top 10 Products")
    top_products = filtered_df.groupby('product_id')['revenue'].sum().nlargest(10).sort_values()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_products.index.astype(str), top_products.values, color='#2ecc71')
    ax.set_xlabel('Revenue ($)')
    ax.set_ylabel('Product ID')
    st.pyplot(fig)
    plt.close()

# --- Data Table ---
st.markdown("---")
st.subheader("Sales Data")

# Show/hide columns
show_columns = st.multiselect(
    "Select columns to display",
    options=filtered_df.columns.tolist(),
    default=['product_id', 'category', 'region', 'quantity', 'revenue', 'date']
)

# Pagination
rows_per_page = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
total_pages = len(filtered_df) // rows_per_page + 1
page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)

start_idx = (page - 1) * rows_per_page
end_idx = start_idx + rows_per_page

st.dataframe(
    filtered_df[show_columns].iloc[start_idx:end_idx],
    use_container_width=True
)

st.caption(f"Showing {start_idx+1}-{min(end_idx, len(filtered_df))} of {len(filtered_df)} records")

# --- Download Section ---
st.markdown("---")
st.subheader("Export Data")

col1, col2 = st.columns(2)

with col1:
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="sales_data.csv",
        mime="text/csv"
    )

with col2:
    # Summary report
    summary = f"""
    Sales Summary Report
    ====================
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    
    Filters Applied:
    - Category: {selected_category}
    - Region: {selected_region}
    - Date Range: {date_range[0]} to {date_range[1] if len(date_range) > 1 else date_range[0]}
    
    Key Metrics:
    - Total Revenue: ${total_revenue:,.2f}
    - Total Transactions: {total_transactions:,}
    - Average Order Value: ${avg_order:.2f}
    - Total Units Sold: {total_units:,}
    
    Revenue by Category:
    {category_rev.to_string()}
    
    Revenue by Region:
    {region_rev.to_string()}
    """
    
    st.download_button(
        label="📄 Download Report",
        data=summary,
        file_name="sales_report.txt",
        mime="text/plain"
    )

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888;'>
        Built with Streamlit | NumPy | Pandas | Matplotlib | Seaborn
    </div>
    """,
    unsafe_allow_html=True
)
