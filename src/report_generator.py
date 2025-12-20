"""
Report Generator - Automated PDF/HTML Reports
Covers: Jinja2 templating, HTML generation, PDF export
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import base64
import io


class ReportGenerator:
    """Generate professional HTML and PDF reports."""
    
    def __init__(self, df, analyzer):
        self.df = df
        self.analyzer = analyzer
        self.generated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _get_summary_stats(self):
        """Calculate summary statistics."""
        return {
            'total_revenue': self.df['revenue'].sum(),
            'total_transactions': len(self.df),
            'avg_order_value': self.df['revenue'].mean(),
            'median_order_value': self.df['revenue'].median(),
            'total_units': self.df['quantity'].sum(),
            'unique_products': self.df['product_id'].nunique(),
            'date_start': self.df['date'].min().strftime('%Y-%m-%d'),
            'date_end': self.df['date'].max().strftime('%Y-%m-%d')
        }
    
    def _get_category_stats(self):
        """Get category performance stats."""
        return self.df.groupby('category', observed=True).agg({
            'revenue': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).round(2)
    
    def _get_regional_stats(self):
        """Get regional performance stats."""
        return self.df.groupby('region', observed=True).agg({
            'revenue': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).round(2)
    
    def _get_monthly_stats(self):
        """Get monthly trend data."""
        monthly = self.df.groupby(self.df['date'].dt.to_period('M')).agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'product_id': 'nunique'
        }).reset_index()
        monthly['date'] = monthly['date'].astype(str)
        monthly.columns = ['Month', 'Revenue', 'Quantity', 'Unique Products']
        return monthly
    
    def _get_top_products(self, n=10):
        """Get top products."""
        return self.df.groupby('product_id').agg({
            'revenue': 'sum',
            'quantity': 'sum'
        }).nlargest(n, 'revenue').round(2).reset_index()
    
    def generate_html_report(self, output_path='outputs/sales_report.html', include_charts=True):
        """Generate comprehensive HTML report."""
        stats = self._get_summary_stats()
        category_stats = self._get_category_stats()
        regional_stats = self._get_regional_stats()
        monthly_stats = self._get_monthly_stats()
        top_products = self._get_top_products()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Analytics Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #3498db;
        }}
        .header h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #7f8c8d;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            color: white;
        }}
        .metric-card.green {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        .metric-card.orange {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        .metric-card.blue {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .metric-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }}
        th {{
            background: #3498db;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .chart-container {{
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .bar {{
            height: 30px;
            background: linear-gradient(90deg, #3498db, #2ecc71);
            border-radius: 4px;
            margin: 8px 0;
            position: relative;
        }}
        .bar-label {{
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            color: #7f8c8d;
        }}
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Sales Analytics Report</h1>
            <p>Generated on {self.generated_at}</p>
            <p>Period: {stats['date_start']} to {stats['date_end']}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">${stats['total_revenue']:,.0f}</div>
                <div class="metric-label">Total Revenue</div>
            </div>
            <div class="metric-card green">
                <div class="metric-value">{stats['total_transactions']:,}</div>
                <div class="metric-label">Transactions</div>
            </div>
            <div class="metric-card orange">
                <div class="metric-value">${stats['avg_order_value']:.2f}</div>
                <div class="metric-label">Avg Order Value</div>
            </div>
            <div class="metric-card blue">
                <div class="metric-value">{stats['total_units']:,}</div>
                <div class="metric-label">Units Sold</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Category Performance</h2>
            {self._generate_category_chart(category_stats)}
            {category_stats.to_html(classes='data-table')}
        </div>
        
        <div class="section">
            <h2>🌍 Regional Performance</h2>
            {regional_stats.to_html(classes='data-table')}
        </div>
        
        <div class="section">
            <h2>📅 Monthly Trend</h2>
            {monthly_stats.to_html(index=False, classes='data-table')}
        </div>
        
        <div class="section">
            <h2>🏆 Top 10 Products</h2>
            {top_products.to_html(index=False, classes='data-table')}
        </div>
        
        <div class="footer">
            <p>Sales Analyzer Project | NumPy + Pandas + Python</p>
        </div>
    </div>
</body>
</html>
"""
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"HTML report saved to: {output_path}")
        return output_path
    
    def _generate_category_chart(self, category_stats):
        """Generate simple CSS bar chart for categories."""
        revenues = category_stats[('revenue', 'sum')]
        max_rev = revenues.max()
        
        html = '<div class="chart-container">'
        for category, revenue in revenues.items():
            width_pct = (revenue / max_rev) * 100
            html += f'''
            <div style="margin: 10px 0;">
                <div style="margin-bottom: 5px;">{category}</div>
                <div class="bar" style="width: {width_pct}%;">
                    <span class="bar-label">${revenue:,.0f}</span>
                </div>
            </div>
            '''
        html += '</div>'
        return html
    
    def generate_markdown_report(self, output_path='outputs/sales_report.md'):
        """Generate Markdown report."""
        stats = self._get_summary_stats()
        
        md = f"""# Sales Analytics Report

**Generated:** {self.generated_at}  
**Period:** {stats['date_start']} to {stats['date_end']}

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Revenue | ${stats['total_revenue']:,.2f} |
| Total Transactions | {stats['total_transactions']:,} |
| Average Order Value | ${stats['avg_order_value']:.2f} |
| Median Order Value | ${stats['median_order_value']:.2f} |
| Total Units Sold | {stats['total_units']:,} |
| Unique Products | {stats['unique_products']} |

---

## Category Performance

{self._get_category_stats().to_markdown()}

---

## Regional Performance

{self._get_regional_stats().to_markdown()}

---

## Monthly Trend

{self._get_monthly_stats().to_markdown(index=False)}

---

## Top 10 Products by Revenue

{self._get_top_products().to_markdown(index=False)}

---

*Report generated by Sales Analyzer*
"""
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"Markdown report saved to: {output_path}")
        return output_path
    
    def generate_excel_report(self, output_path='outputs/sales_report.xlsx'):
        """Generate Excel report with multiple sheets."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary sheet
            summary_df = pd.DataFrame([self._get_summary_stats()]).T
            summary_df.columns = ['Value']
            summary_df.to_excel(writer, sheet_name='Summary')
            
            # Raw data
            self.df.to_excel(writer, sheet_name='Raw Data', index=False)
            
            # Category stats
            self._get_category_stats().to_excel(writer, sheet_name='By Category')
            
            # Regional stats
            self._get_regional_stats().to_excel(writer, sheet_name='By Region')
            
            # Monthly trend
            self._get_monthly_stats().to_excel(writer, sheet_name='Monthly Trend', index=False)
            
            # Top products
            self._get_top_products(20).to_excel(writer, sheet_name='Top Products', index=False)
        
        print(f"Excel report saved to: {output_path}")
        return output_path


if __name__ == "__main__":
    from data_generator import generate_sales_data
    from data_processor import process_sales_data
    from analyzer import SalesAnalyzer
    
    # Generate data
    raw = generate_sales_data(1000)
    df = process_sales_data(raw)
    analyzer = SalesAnalyzer(df)
    
    # Generate reports
    report_gen = ReportGenerator(df, analyzer)
    
    report_gen.generate_html_report()
    report_gen.generate_markdown_report()
    
    # Excel requires openpyxl
    try:
        report_gen.generate_excel_report()
    except ImportError:
        print("Install openpyxl for Excel export: pip install openpyxl")
    
    print("\nAll reports generated!")
