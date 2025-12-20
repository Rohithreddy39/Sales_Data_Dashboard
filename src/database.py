"""
Database Module - SQLite Integration
Covers: CRUD operations, SQL queries, Pandas-SQL integration
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from contextlib import contextmanager


class SalesDatabase:
    """SQLite database manager for sales data."""
    
    def __init__(self, db_path='data/sales.db'):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_tables()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def _init_tables(self):
        """Initialize database tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Sales transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    discount REAL DEFAULT 0,
                    final_price REAL NOT NULL,
                    revenue REAL NOT NULL,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    region TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    product_name TEXT NOT NULL,
                    cost REAL NOT NULL,
                    category TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Daily aggregates table (for faster reporting)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_summary (
                    date TEXT PRIMARY KEY,
                    total_revenue REAL,
                    total_quantity INTEGER,
                    transaction_count INTEGER,
                    avg_order_value REAL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def insert_sales_data(self, df):
        """Insert sales DataFrame into database."""
        with self.get_connection() as conn:
            # Prepare data
            sales_df = df[['product_id', 'quantity', 'unit_price', 'discount',
                          'final_price', 'revenue', 'date', 'category', 'region']].copy()
            sales_df['date'] = sales_df['date'].astype(str)
            sales_df['category'] = sales_df['category'].astype(str)
            sales_df['region'] = sales_df['region'].astype(str)
            
            # Insert to database
            sales_df.to_sql('sales', conn, if_exists='append', index=False)
            
            # Update daily summary
            self._update_daily_summary(conn)
            
            print(f"Inserted {len(df)} records into database")
    
    def _update_daily_summary(self, conn):
        """Update daily summary table."""
        query = '''
            INSERT OR REPLACE INTO daily_summary 
            (date, total_revenue, total_quantity, transaction_count, avg_order_value)
            SELECT 
                date,
                SUM(revenue) as total_revenue,
                SUM(quantity) as total_quantity,
                COUNT(*) as transaction_count,
                AVG(revenue) as avg_order_value
            FROM sales
            GROUP BY date
        '''
        conn.execute(query)
        conn.commit()
    
    def get_all_sales(self):
        """Retrieve all sales as DataFrame."""
        with self.get_connection() as conn:
            return pd.read_sql('SELECT * FROM sales', conn)
    
    def query(self, sql, params=None):
        """Execute custom SQL query and return DataFrame."""
        with self.get_connection() as conn:
            return pd.read_sql(sql, conn, params=params)
    
    def execute(self, sql, params=None):
        """Execute SQL statement (INSERT, UPDATE, DELETE)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            conn.commit()
            return cursor.rowcount
    
    # --- Pre-built Analytics Queries ---
    
    def get_revenue_by_category(self):
        """Get revenue breakdown by category."""
        sql = '''
            SELECT 
                category,
                SUM(revenue) as total_revenue,
                AVG(revenue) as avg_revenue,
                COUNT(*) as transactions
            FROM sales
            GROUP BY category
            ORDER BY total_revenue DESC
        '''
        return self.query(sql)
    
    def get_revenue_by_region(self):
        """Get revenue breakdown by region."""
        sql = '''
            SELECT 
                region,
                SUM(revenue) as total_revenue,
                SUM(quantity) as total_units,
                COUNT(*) as transactions
            FROM sales
            GROUP BY region
            ORDER BY total_revenue DESC
        '''
        return self.query(sql)
    
    def get_monthly_trend(self):
        """Get monthly revenue trend."""
        sql = '''
            SELECT 
                strftime('%Y-%m', date) as month,
                SUM(revenue) as total_revenue,
                SUM(quantity) as total_quantity,
                COUNT(*) as transactions,
                AVG(revenue) as avg_order_value
            FROM sales
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month
        '''
        return self.query(sql)
    
    def get_top_products(self, n=10):
        """Get top N products by revenue."""
        sql = '''
            SELECT 
                product_id,
                SUM(revenue) as total_revenue,
                SUM(quantity) as total_quantity,
                AVG(discount) as avg_discount,
                COUNT(*) as transactions
            FROM sales
            GROUP BY product_id
            ORDER BY total_revenue DESC
            LIMIT ?
        '''
        return self.query(sql, (n,))
    
    def get_daily_summary(self, start_date=None, end_date=None):
        """Get daily summary with optional date filter."""
        sql = 'SELECT * FROM daily_summary'
        conditions = []
        params = []
        
        if start_date:
            conditions.append('date >= ?')
            params.append(start_date)
        if end_date:
            conditions.append('date <= ?')
            params.append(end_date)
        
        if conditions:
            sql += ' WHERE ' + ' AND '.join(conditions)
        
        sql += ' ORDER BY date'
        return self.query(sql, params if params else None)
    
    def search_sales(self, category=None, region=None, min_revenue=None, max_revenue=None):
        """Search sales with filters."""
        sql = 'SELECT * FROM sales WHERE 1=1'
        params = []
        
        if category:
            sql += ' AND category = ?'
            params.append(category)
        if region:
            sql += ' AND region = ?'
            params.append(region)
        if min_revenue:
            sql += ' AND revenue >= ?'
            params.append(min_revenue)
        if max_revenue:
            sql += ' AND revenue <= ?'
            params.append(max_revenue)
        
        return self.query(sql, params if params else None)
    
    def get_stats(self):
        """Get database statistics."""
        with self.get_connection() as conn:
            stats = {}
            
            # Total records
            stats['total_records'] = conn.execute(
                'SELECT COUNT(*) FROM sales'
            ).fetchone()[0]
            
            # Date range
            result = conn.execute(
                'SELECT MIN(date), MAX(date) FROM sales'
            ).fetchone()
            stats['date_range'] = {'start': result[0], 'end': result[1]}
            
            # Total revenue
            stats['total_revenue'] = conn.execute(
                'SELECT SUM(revenue) FROM sales'
            ).fetchone()[0]
            
            # Categories
            stats['categories'] = conn.execute(
                'SELECT DISTINCT category FROM sales'
            ).fetchall()
            
            return stats
    
    def clear_all_data(self):
        """Clear all data from tables (use with caution!)."""
        with self.get_connection() as conn:
            conn.execute('DELETE FROM sales')
            conn.execute('DELETE FROM daily_summary')
            conn.commit()
            print("All data cleared from database")


# --- SQL Practice Examples ---

def demonstrate_sql_queries(db):
    """Demonstrate various SQL queries."""
    print("\n=== SQL Query Examples ===\n")
    
    # 1. Basic SELECT
    print("1. Basic SELECT with LIMIT:")
    print(db.query('SELECT * FROM sales LIMIT 5'))
    
    # 2. Aggregation
    print("\n2. Aggregation (SUM, AVG, COUNT):")
    sql = '''
        SELECT 
            category,
            COUNT(*) as count,
            ROUND(SUM(revenue), 2) as total,
            ROUND(AVG(revenue), 2) as average
        FROM sales
        GROUP BY category
    '''
    print(db.query(sql))
    
    # 3. JOIN (if products table has data)
    print("\n3. Subquery - Above average revenue:")
    sql = '''
        SELECT * FROM sales 
        WHERE revenue > (SELECT AVG(revenue) FROM sales)
        LIMIT 5
    '''
    print(db.query(sql))
    
    # 4. Window function
    print("\n4. Running total by date:")
    sql = '''
        SELECT 
            date,
            total_revenue,
            SUM(total_revenue) OVER (ORDER BY date) as running_total
        FROM daily_summary
        LIMIT 10
    '''
    print(db.query(sql))
    
    # 5. CASE statement
    print("\n5. Revenue tiers using CASE:")
    sql = '''
        SELECT 
            CASE 
                WHEN revenue > 500 THEN 'High'
                WHEN revenue > 200 THEN 'Medium'
                ELSE 'Low'
            END as tier,
            COUNT(*) as count,
            ROUND(AVG(revenue), 2) as avg_revenue
        FROM sales
        GROUP BY tier
    '''
    print(db.query(sql))


if __name__ == "__main__":
    from data_generator import generate_sales_data
    from data_processor import process_sales_data
    
    # Generate data
    raw = generate_sales_data(1000)
    df = process_sales_data(raw)
    
    # Initialize database
    db = SalesDatabase('data/sales.db')
    
    # Clear and insert fresh data
    db.clear_all_data()
    db.insert_sales_data(df)
    
    # Show stats
    print("\nDatabase Stats:")
    print(db.get_stats())
    
    # Run queries
    print("\nRevenue by Category:")
    print(db.get_revenue_by_category())
    
    print("\nTop 5 Products:")
    print(db.get_top_products(5))
    
    # Demonstrate SQL
    demonstrate_sql_queries(db)
