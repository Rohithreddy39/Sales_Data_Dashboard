"""
Sales Analyzer Module - Combining NumPy and Pandas
Covers: Analysis, aggregation, reporting, advanced operations
"""

import pandas as pd
import numpy as np
from typing import Optional


class SalesAnalyzer:
    """
    A class to analyze sales data.
    Demonstrates OOP with Pandas/NumPy.
    """
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with a sales DataFrame."""
        self.df = df
        self._validate_data()
    
    def _validate_data(self):
        """Validate required columns exist."""
        required = ['revenue', 'quantity', 'category', 'region', 'date']
        missing = [col for col in required if col not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    
    def get_summary(self) -> pd.DataFrame:
        """
        Get overall summary statistics.
        Uses both NumPy and Pandas methods.
        """
        summary = {
            'Total Revenue': f"${self.df['revenue'].sum():,.2f}",
            'Total Transactions': len(self.df),
            'Total Units Sold': self.df['quantity'].sum(),
            'Average Order Value': f"${self.df['revenue'].mean():,.2f}",
            'Median Order Value': f"${self.df['revenue'].median():,.2f}",
            'Std Deviation': f"${self.df['revenue'].std():,.2f}",
            'Date Range': f"{self.df['date'].min().date()} to {self.df['date'].max().date()}"
        }
        return pd.DataFrame(list(summary.items()), columns=['Metric', 'Value'])
    
    def top_products(self, n: int = 10) -> pd.DataFrame:
        """Get top N products by revenue."""
        return (
            self.df
            .groupby('product_id')
            .agg({
                'revenue': 'sum',
                'quantity': 'sum',
                'discount': 'mean'
            })
            .sort_values('revenue', ascending=False)
            .head(n)
            .round(2)
            .reset_index()
        )
    
    def monthly_trend(self) -> pd.DataFrame:
        """Analyze monthly sales trend."""
        monthly = (
            self.df
            .groupby(['year', 'month', 'month_name'])
            .agg({
                'revenue': 'sum',
                'quantity': 'sum',
                'product_id': 'nunique'
            })
            .rename(columns={'product_id': 'unique_products'})
            .reset_index()
        )
        
        # Calculate month-over-month growth using NumPy
        monthly['mom_growth'] = np.round(
            monthly['revenue'].pct_change() * 100, 2
        )
        
        return monthly
    
    def category_performance(self) -> pd.DataFrame:
        """Analyze performance by category."""
        return (
            self.df
            .groupby('category')
            .agg({
                'revenue': ['sum', 'mean', 'std'],
                'quantity': 'sum',
                'product_id': 'nunique',
                'discount': 'mean'
            })
            .round(2)
        )
    
    def regional_analysis(self) -> pd.DataFrame:
        """Analyze performance by region."""
        regional = (
            self.df
            .groupby('region')
            .agg({
                'revenue': ['sum', 'mean', 'count'],
                'quantity': 'sum'
            })
            .round(2)
        )
        
        # Calculate percentage of total
        total_revenue = self.df['revenue'].sum()
        regional[('revenue', 'pct_of_total')] = (
            regional[('revenue', 'sum')] / total_revenue * 100
        ).round(2)
        
        return regional
    
    def weekly_pattern(self) -> pd.DataFrame:
        """Analyze sales patterns by day of week."""
        day_order = ['Monday', 'Tuesday', 'Wednesday', 
                     'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        weekly = (
            self.df
            .groupby('day_of_week')
            .agg({
                'revenue': ['sum', 'mean', 'count']
            })
            .round(2)
        )
        
        # Reorder by day of week
        weekly = weekly.reindex(day_order)
        return weekly
    
    def cohort_analysis(self) -> pd.DataFrame:
        """
        Simple cohort analysis by quarter.
        Demonstrates advanced grouping.
        """
        return (
            self.df
            .groupby(['quarter', 'category'])
            .agg({
                'revenue': 'sum',
                'quantity': 'sum'
            })
            .unstack(fill_value=0)
            .round(2)
        )
    
    def find_outliers(self, column: str = 'revenue', 
                      method: str = 'iqr') -> pd.DataFrame:
        """
        Find outliers using IQR or Z-score method.
        Demonstrates NumPy statistical operations.
        """
        data = self.df[column].values
        
        if method == 'iqr':
            q1 = np.percentile(data, 25)
            q3 = np.percentile(data, 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            mask = (data < lower_bound) | (data > upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs((data - np.mean(data)) / np.std(data))
            mask = z_scores > 3
        
        else:
            raise ValueError("Method must be 'iqr' or 'zscore'")
        
        outliers = self.df[mask].copy()
        outliers['outlier_value'] = data[mask]
        
        return outliers
    
    def calculate_percentiles(self, column: str = 'revenue') -> dict:
        """Calculate various percentiles using NumPy."""
        data = self.df[column].values
        percentiles = [10, 25, 50, 75, 90, 95, 99]
        
        return {
            f'p{p}': np.percentile(data, p)
            for p in percentiles
        }
    
    def correlation_matrix(self) -> pd.DataFrame:
        """
        Calculate correlation matrix for numeric columns.
        Uses NumPy's corrcoef under the hood.
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        return self.df[numeric_cols].corr().round(3)
    
    def export_report(self, filepath: str):
        """Export analysis results to CSV."""
        # Combine key metrics
        report = self.df.groupby(['category', 'region']).agg({
            'revenue': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'discount': 'mean'
        }).round(2)
        
        report.to_csv(filepath)
        return report
    
    def custom_analysis(self, group_by: list, 
                        agg_dict: dict) -> pd.DataFrame:
        """
        Flexible custom analysis.
        
        Example:
            analyzer.custom_analysis(
                group_by=['category', 'month'],
                agg_dict={'revenue': 'sum', 'quantity': 'mean'}
            )
        """
        return (
            self.df
            .groupby(group_by)
            .agg(agg_dict)
            .round(2)
            .reset_index()
        )


# --- Advanced NumPy/Pandas Combinations ---

def demonstrate_advanced_operations(df: pd.DataFrame):
    """
    Advanced operations combining NumPy and Pandas.
    """
    print("\n=== Advanced Operations ===\n")
    
    # 1. Vectorized conditions with np.select
    print("1. np.select for multiple conditions:")
    conditions = [
        df['revenue'] > 500,
        df['revenue'] > 200,
        df['revenue'] > 100
    ]
    choices = ['Premium', 'Standard', 'Basic']
    df['customer_tier'] = np.select(conditions, choices, default='Entry')
    print(df['customer_tier'].value_counts())
    
    # 2. Cumulative operations
    print("\n2. Cumulative Revenue by Date:")
    daily = df.groupby('date')['revenue'].sum().reset_index()
    daily['cumulative_revenue'] = np.cumsum(daily['revenue'])
    print(daily.tail())
    
    # 3. Binning with pd.cut and np.histogram
    print("\n3. Revenue Binning:")
    df['revenue_bin'] = pd.cut(
        df['revenue'],
        bins=[0, 100, 250, 500, 1000, np.inf],
        labels=['0-100', '100-250', '250-500', '500-1000', '1000+']
    )
    print(df['revenue_bin'].value_counts().sort_index())
    
    # 4. Ranking
    print("\n4. Ranking Products:")
    product_revenue = df.groupby('product_id')['revenue'].sum()
    rankings = product_revenue.rank(ascending=False).astype(int)
    top_5 = rankings[rankings <= 5].sort_values()
    print(f"Top 5 products: {top_5.index.tolist()}")
    
    # 5. Window functions
    print("\n5. Rolling Statistics:")
    daily_revenue = df.groupby('date')['revenue'].sum().reset_index()
    daily_revenue['rolling_mean'] = daily_revenue['revenue'].rolling(7).mean()
    daily_revenue['rolling_std'] = daily_revenue['revenue'].rolling(7).std()
    daily_revenue['expanding_mean'] = daily_revenue['revenue'].expanding().mean()
    print(daily_revenue.tail(10))
    
    return df


if __name__ == "__main__":
    # Test the analyzer
    from data_generator import generate_sales_data
    from data_processor import process_sales_data
    
    raw = generate_sales_data(1000)
    df = process_sales_data(raw)
    
    analyzer = SalesAnalyzer(df)
    
    print("Summary:")
    print(analyzer.get_summary())
    
    print("\nTop Products:")
    print(analyzer.top_products(5))
    
    print("\nPercentiles:")
    print(analyzer.calculate_percentiles())
    
    print("\nOutliers (IQR method):")
    outliers = analyzer.find_outliers()
    print(f"Found {len(outliers)} outliers")
    
    # Run advanced demo
    demonstrate_advanced_operations(df)
