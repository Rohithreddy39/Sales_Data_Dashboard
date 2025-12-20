"""
Data Generator Module - NumPy Fundamentals
Covers: arrays, random generation, mathematical operations, broadcasting
"""

import numpy as np
from datetime import datetime, timedelta


def generate_sales_data(num_records: int = 1000, seed: int = 42) -> dict:
    """
    Generate synthetic sales data using NumPy.
    
    NumPy concepts covered:
    - np.random for random data generation
    - Array creation and manipulation
    - Vectorized operations
    - Broadcasting
    - Statistical functions
    """
    # Set seed for reproducibility
    np.random.seed(seed)
    
    # --- Array Creation ---
    # Generate product IDs (1 to 50 products)
    product_ids = np.random.randint(1, 51, size=num_records)
    
    # Generate quantities (1 to 20 units)
    quantities = np.random.randint(1, 21, size=num_records)
    
    # --- Random Distributions ---
    # Generate prices using normal distribution (mean=50, std=20)
    base_prices = np.random.normal(loc=50, scale=20, size=num_records)
    # Clip to ensure no negative prices (min $10, max $200)
    prices = np.clip(base_prices, 10, 200)
    
    # Generate discount percentages (0% to 30%)
    discounts = np.random.uniform(0, 0.30, size=num_records)
    
    # --- Vectorized Operations ---
    # Calculate final prices after discount (broadcasting in action)
    final_prices = prices * (1 - discounts)
    
    # Calculate revenue for each transaction
    revenue = final_prices * quantities
    
    # --- Date Generation ---
    # Generate random dates for the past year
    start_date = datetime(2024, 1, 1)
    days_offset = np.random.randint(0, 365, size=num_records)
    dates = np.array([start_date + timedelta(days=int(d)) for d in days_offset])
    
    # --- Categorical Data ---
    # Assign categories based on product_id ranges
    categories = np.where(
        product_ids <= 15, 'Electronics',
        np.where(
            product_ids <= 30, 'Clothing',
            np.where(
                product_ids <= 40, 'Home & Garden',
                'Sports'
            )
        )
    )
    
    # Assign regions
    regions = np.random.choice(
        ['North', 'South', 'East', 'West'], 
        size=num_records,
        p=[0.3, 0.25, 0.25, 0.2]  # Weighted probabilities
    )
    
    # --- Statistical Summary (NumPy stats functions) ---
    print(f"    Revenue Stats: Mean=${np.mean(revenue):.2f}, "
          f"Std=${np.std(revenue):.2f}, "
          f"Total=${np.sum(revenue):.2f}")
    
    return {
        'product_id': product_ids,
        'quantity': quantities,
        'unit_price': np.round(prices, 2),
        'discount': np.round(discounts, 4),
        'final_price': np.round(final_prices, 2),
        'revenue': np.round(revenue, 2),
        'date': dates,
        'category': categories,
        'region': regions
    }


def generate_product_catalog(num_products: int = 50) -> dict:
    """
    Generate a product catalog.
    Demonstrates: structured arrays, string operations
    """
    np.random.seed(42)
    
    product_ids = np.arange(1, num_products + 1)
    
    # Generate product names
    prefixes = ['Pro', 'Ultra', 'Basic', 'Premium', 'Elite']
    suffixes = ['Widget', 'Gadget', 'Tool', 'Device', 'Kit']
    
    names = np.array([
        f"{np.random.choice(prefixes)} {np.random.choice(suffixes)} {i}"
        for i in product_ids
    ])
    
    # Base costs (for profit calculation later)
    costs = np.random.uniform(5, 100, size=num_products)
    
    return {
        'product_id': product_ids,
        'product_name': names,
        'cost': np.round(costs, 2)
    }


# --- NumPy Practice Functions ---

def demonstrate_numpy_operations():
    """
    Additional NumPy operations for learning.
    Run this to see various NumPy features in action.
    """
    print("\n=== NumPy Operations Demo ===\n")
    
    # 1. Array Creation Methods
    print("1. Array Creation:")
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.zeros((3, 3))
    arr3 = np.ones((2, 4))
    arr4 = np.arange(0, 10, 2)
    arr5 = np.linspace(0, 1, 5)
    print(f"   arange(0,10,2): {arr4}")
    print(f"   linspace(0,1,5): {arr5}")
    
    # 2. Array Reshaping
    print("\n2. Reshaping:")
    arr = np.arange(12)
    reshaped = arr.reshape(3, 4)
    print(f"   Original: {arr}")
    print(f"   Reshaped (3x4):\n{reshaped}")
    
    # 3. Broadcasting
    print("\n3. Broadcasting:")
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    scalar = 10
    result = matrix * scalar
    print(f"   Matrix * 10:\n{result}")
    
    # 4. Aggregation
    print("\n4. Aggregation:")
    data = np.random.randint(1, 100, size=(4, 5))
    print(f"   Data:\n{data}")
    print(f"   Sum: {np.sum(data)}")
    print(f"   Mean per column: {np.mean(data, axis=0)}")
    print(f"   Max per row: {np.max(data, axis=1)}")
    
    # 5. Boolean Indexing
    print("\n5. Boolean Indexing:")
    arr = np.array([10, 25, 30, 45, 50, 65])
    mask = arr > 30
    print(f"   Array: {arr}")
    print(f"   Values > 30: {arr[mask]}")
    
    # 6. Fancy Indexing
    print("\n6. Fancy Indexing:")
    arr = np.array([10, 20, 30, 40, 50])
    indices = np.array([0, 2, 4])
    print(f"   Array: {arr}")
    print(f"   Elements at [0,2,4]: {arr[indices]}")


if __name__ == "__main__":
    # Test the generator
    data = generate_sales_data(100)
    print(f"\nGenerated {len(data['product_id'])} records")
    
    # Run NumPy demo
    demonstrate_numpy_operations()
