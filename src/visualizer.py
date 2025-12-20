"""
Visualization Module - Matplotlib & Seaborn
Covers: Charts, plots, styling, subplots, saving figures
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path


class SalesVisualizer:
    """Create professional visualizations for sales data."""
    
    def __init__(self, df, style='seaborn-v0_8-whitegrid'):
        self.df = df
        self.setup_style(style)
        self.colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f39c12']
        
    def setup_style(self, style):
        """Configure plot styling."""
        try:
            plt.style.use(style)
        except:
            plt.style.use('seaborn-v0_8')
        
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
    
    def revenue_by_category(self, save_path=None):
        """Bar chart: Revenue by category."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        category_rev = self.df.groupby('category', observed=True)['revenue'].sum().sort_values(ascending=True)
        
        bars = ax.barh(category_rev.index, category_rev.values, color=self.colors)
        
        # Add value labels
        for bar, value in zip(bars, category_rev.values):
            ax.text(value + 1000, bar.get_y() + bar.get_height()/2, 
                   f'${value:,.0f}', va='center', fontsize=10)
        
        ax.set_xlabel('Total Revenue ($)')
        ax.set_title('Revenue by Product Category')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    def monthly_trend(self, save_path=None):
        """Line chart: Monthly revenue trend."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        monthly = self.df.groupby(['year', 'month']).agg({
            'revenue': 'sum',
            'quantity': 'sum'
        }).reset_index()
        monthly['period'] = monthly['year'].astype(str) + '-' + monthly['month'].astype(str).str.zfill(2)
        
        # Primary axis - Revenue
        color1 = '#3498db'
        ax.plot(monthly['period'], monthly['revenue'], marker='o', 
                linewidth=2, color=color1, label='Revenue')
        ax.fill_between(monthly['period'], monthly['revenue'], alpha=0.3, color=color1)
        ax.set_xlabel('Month')
        ax.set_ylabel('Revenue ($)', color=color1)
        ax.tick_params(axis='y', labelcolor=color1)
        
        # Secondary axis - Quantity
        ax2 = ax.twinx()
        color2 = '#e74c3c'
        ax2.plot(monthly['period'], monthly['quantity'], marker='s', 
                linewidth=2, color=color2, linestyle='--', label='Quantity')
        ax2.set_ylabel('Units Sold', color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        
        ax.set_title('Monthly Sales Trend')
        plt.xticks(rotation=45)
        
        # Combined legend
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    def revenue_distribution(self, save_path=None):
        """Histogram + KDE: Revenue distribution."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram with KDE
        sns.histplot(data=self.df, x='revenue', kde=True, ax=axes[0], color='#3498db')
        axes[0].set_title('Revenue Distribution')
        axes[0].set_xlabel('Revenue ($)')
        
        # Box plot by category
        sns.boxplot(data=self.df, x='category', y='revenue', ax=axes[1], palette='Set2')
        axes[1].set_title('Revenue Distribution by Category')
        axes[1].set_xlabel('Category')
        axes[1].set_ylabel('Revenue ($)')
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    def regional_performance(self, save_path=None):
        """Pie chart + Bar: Regional analysis."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        regional = self.df.groupby('region', observed=True)['revenue'].sum()
        
        # Pie chart
        axes[0].pie(regional.values, labels=regional.index, autopct='%1.1f%%',
                   colors=self.colors, explode=[0.02]*len(regional))
        axes[0].set_title('Revenue Share by Region')
        
        # Stacked bar by category and region
        pivot = self.df.pivot_table(
            values='revenue', 
            index='region', 
            columns='category', 
            aggfunc='sum',
            observed=True
        )
        pivot.plot(kind='bar', stacked=True, ax=axes[1], colormap='Set2')
        axes[1].set_title('Revenue by Region and Category')
        axes[1].set_xlabel('Region')
        axes[1].set_ylabel('Revenue ($)')
        axes[1].legend(title='Category', bbox_to_anchor=(1.02, 1))
        axes[1].tick_params(axis='x', rotation=0)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    def correlation_heatmap(self, save_path=None):
        """Heatmap: Correlation matrix."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
                   cmap='RdYlBu_r', center=0, ax=ax,
                   square=True, linewidths=0.5)
        ax.set_title('Feature Correlation Matrix')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    def top_products_chart(self, n=10, save_path=None):
        """Horizontal bar: Top products."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        top = self.df.groupby('product_id')['revenue'].sum().nlargest(n).sort_values()
        
        colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(top)))
        bars = ax.barh(top.index.astype(str), top.values, color=colors)
        
        for bar, value in zip(bars, top.values):
            ax.text(value + 100, bar.get_y() + bar.get_height()/2,
                   f'${value:,.0f}', va='center', fontsize=9)
        
        ax.set_xlabel('Total Revenue ($)')
        ax.set_ylabel('Product ID')
        ax.set_title(f'Top {n} Products by Revenue')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    def day_of_week_pattern(self, save_path=None):
        """Bar chart: Sales by day of week."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                     'Friday', 'Saturday', 'Sunday']
        
        daily = self.df.groupby('day_of_week')['revenue'].agg(['sum', 'mean', 'count'])
        daily = daily.reindex(day_order)
        
        x = np.arange(len(day_order))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, daily['sum']/1000, width, label='Total Revenue (K$)', color='#3498db')
        
        ax2 = ax.twinx()
        bars2 = ax2.bar(x + width/2, daily['count'], width, label='Transactions', color='#e74c3c', alpha=0.7)
        
        ax.set_xlabel('Day of Week')
        ax.set_ylabel('Revenue ($K)', color='#3498db')
        ax2.set_ylabel('Transaction Count', color='#e74c3c')
        ax.set_xticks(x)
        ax.set_xticklabels(day_order, rotation=45)
        ax.set_title('Sales Pattern by Day of Week')
        
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    def scatter_analysis(self, save_path=None):
        """Scatter plots: Relationship analysis."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Quantity vs Revenue
        sns.scatterplot(data=self.df, x='quantity', y='revenue', 
                       hue='category', alpha=0.6, ax=axes[0])
        axes[0].set_title('Quantity vs Revenue')
        
        # Discount vs Revenue
        sns.scatterplot(data=self.df, x='discount', y='revenue',
                       hue='category', alpha=0.6, ax=axes[1])
        axes[1].set_title('Discount vs Revenue')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    def generate_dashboard(self, output_dir='outputs/charts'):
        """Generate all charts and save to directory."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        charts = {
            'revenue_by_category': self.revenue_by_category,
            'monthly_trend': self.monthly_trend,
            'revenue_distribution': self.revenue_distribution,
            'regional_performance': self.regional_performance,
            'correlation_heatmap': self.correlation_heatmap,
            'top_products': self.top_products_chart,
            'day_of_week': self.day_of_week_pattern,
            'scatter_analysis': self.scatter_analysis
        }
        
        saved_files = []
        for name, func in charts.items():
            filepath = f'{output_dir}/{name}.png'
            func(save_path=filepath)
            saved_files.append(filepath)
            print(f'Saved: {filepath}')
            plt.close()
        
        return saved_files


if __name__ == "__main__":
    from data_generator import generate_sales_data
    from data_processor import process_sales_data
    
    # Generate and process data
    raw = generate_sales_data(1000)
    df = process_sales_data(raw)
    
    # Create visualizer
    viz = SalesVisualizer(df)
    
    # Generate all charts
    viz.generate_dashboard()
    
    print("\nAll charts generated successfully!")
