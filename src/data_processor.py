"""
Data Processor Module - Pandas Fundamentals
Covers: DataFrames, cleaning, transformation, grouping, merging
"""

import pandas as pd
import numpy as np
from datetime import datetime


def process_sales_data(raw_data: dict) -> pd.DataFrame:
    """
    Process raw numpy data into a clean Pandas DataFrame.
    
    Pandas concepts covered:
    - DataFrame creation
    - Data type conversion
    - Column operations
    - DateTime handling
    """
    # --- DataFrame Creation ---
    df = pd.DataFrame(raw_data)
    
    # --- Data Type Conversion ---
    df['date'] = pd.to_datetime(df['date'])
    df['product_id'] = df['product_id'].astype('int32')
    df['category'] = df['category'].astype('category')
    df['region'] = df['region'].astype('category')
    
    # --- Feature Engineering ---
    # Extract date components
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name()
    df['day_of_week'] = df['date'].dt.day_name()
    df['quarter'] = df['date'].dt.quarter
    
    # Create derived columns
    df['discount_amount'] = df['unit_price'] * df['discount']
    df['is_high_value'] = df['revenue'] > df['revenue'].median()
    
    # --- Sorting ---
    df = df.sort_values('date').reset_index(drop=True)
    
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate DataFrame.
    
    Covers:
    - Handling missing values
    - Removing duplicates
    - Data validation
    """
    df_clean = df.copy()
    
    # Check for missing values
    missing = df_clean.isnull().sum()
    if missing.any():
        print(f"Missing values found:\n{missing[missing > 0]}")
        # Fill numeric columns with median
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(
            df_clean[numeric_cols].median()
        )
    
    # Remove duplicates
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    removed = initial_rows - len(df_clean)
    if removed > 0:
        print(f"Removed {removed} duplicate rows")
    
    # Validate data ranges
    df_clean = df_clean[df_clean['revenue'] >= 0]
    df_clean = df_clean[df_clean['quantity'] > 0]
    
    return df_clean


def merge_with_catalog(sales_df: pd.DataFrame, catalog_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge sales data with product catalog.
    
    Covers:
    - Different types of merges (inner, left, right, outer)
    - Handling merge keys
    """
    # Left merge to keep all sales records
    merged = pd.merge(
        sales_df,
        catalog_df,
        on='product_id',
        how='left'
    )
    
    # Calculate profit if cost is available
    if 'cost' in merged.columns:
        merged['profit'] = merged['revenue'] - (merged['cost'] * merged['quantity'])
        merged['profit_margin'] = (merged['profit'] / merged['revenue']) * 100
    
    return merged


# --- Pandas Practice Functions ---

def demonstrate_pandas_operations(df: pd.DataFrame):
    """
    Demonstrate various Pandas operations.
    """
    print("\n=== Pandas Operations Demo ===\n")
    
    # 1. Basic Info
    print("1. DataFrame Info:")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Memory: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    # 2. Selection
    print("\n2. Selection Methods:")
    print(f"   Single column (head): {df['revenue'].head(3).tolist()}")
    print(f"   Multiple columns:\n{df[['product_id', 'revenue', 'category']].head(3)}")
    
    # 3. Filtering
    print("\n3. Filtering:")
    high_revenue = df[df['revenue'] > 500]
    print(f"   Transactions > $500: {len(high_revenue)}")
    
    electronics = df[df['category'] == 'Electronics']
    print(f"   Electronics transactions: {len(electronics)}")
    
    # Complex filter
    complex_filter = df[
        (df['category'] == 'Electronics') & 
        (df['revenue'] > 300) &
        (df['region'] == 'North')
    ]
    print(f"   Electronics > $300 in North: {len(complex_filter)}")
    
    # 4. GroupBy
    print("\n4. GroupBy Operations:")
    category_stats = df.groupby('category').agg({
        'revenue': ['sum', 'mean', 'count'],
        'quantity': 'sum'
    }).round(2)
    print(category_stats)
    
    # 5. Pivot Tables
    print("\n5. Pivot Table:")
    pivot = pd.pivot_table(
        df,
        values='revenue',
        index='category',
        columns='region',
        aggfunc='sum'
    ).round(2)
    print(pivot)
    
    # 6. Apply and Lambda
    print("\n6. Apply/Lambda:")
    df['revenue_tier'] = df['revenue'].apply(
        lambda x: 'High' if x > 500 else ('Medium' if x > 200 else 'Low')
    )
    print(df['revenue_tier'].value_counts())
    
    # 7. String Operations
    print("\n7. String Operations:")
    df['category_upper'] = df['category'].astype(str).str.upper()
    print(f"   Upper categories: {df['category_upper'].unique()[:3]}")
    
    # 8. Rolling/Window Functions
    print("\n8. Rolling Calculations:")
    daily_revenue = df.groupby('date')['revenue'].sum().reset_index()
    daily_revenue['rolling_7day'] = daily_revenue['revenue'].rolling(window=7).mean()
    print(daily_revenue.tail())
    
    return df


def demonstrate_data_cleaning():
    """
    Demonstrate data cleaning techniques.
    """
    print("\n=== Data Cleaning Demo ===\n")
    
    # Create messy data
    messy_data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Alice', None, 'Eve'],
        'age': [25, None, 35, 25, 28, -5],
        'salary': [50000, 60000, None, 50000, 55000, 70000],
        'department': ['Sales', 'IT', 'Sales', 'Sales', 'HR', 'IT']
    })
    
    print("Original messy data:")
    print(messy_data)
    
    # 1. Handle missing values
    print("\n1. Missing values:")
    print(messy_data.isnull().sum())
    
    # Fill with median for numeric
    messy_data['age'] = messy_data['age'].fillna(messy_data['age'].median())
    messy_data['salary'] = messy_data['salary'].fillna(messy_data['salary'].median())
    
    # Fill with mode for categorical
    messy_data['name'] = messy_data['name'].fillna('Unknown')
    
    # 2. Remove duplicates
    print(f"\n2. Duplicates: {messy_data.duplicated().sum()}")
    messy_data = messy_data.drop_duplicates()
    
    # 3. Fix invalid values
    messy_data.loc[messy_data['age'] < 0, 'age'] = messy_data['age'].median()
    
    print("\nCleaned data:")
    print(messy_data)


if __name__ == "__main__":
    # Test the processor
    from data_generator import generate_sales_data
    
    raw = generate_sales_data(500)
    df = process_sales_data(raw)
    
    print(f"\nProcessed DataFrame:")
    print(df.head())
    print(f"\nData types:\n{df.dtypes}")
    
    # Run demos
    demonstrate_pandas_operations(df)
    demonstrate_data_cleaning()
