"""
Sales Data Analyzer - Extended Version
Covers: NumPy, Pandas, Visualization, Database, Reporting
"""

import argparse
from pathlib import Path

from src.data_generator import generate_sales_data, generate_product_catalog
from src.data_processor import process_sales_data
from src.analyzer import SalesAnalyzer


def run_basic_analysis(num_records=1000):
    """Run basic analysis pipeline."""
    print("=" * 60)
    print("Sales Data Analyzer - Basic Analysis")
    print("=" * 60)
    
    # Generate data
    print("\n[1] Generating sales data...")
    raw_data = generate_sales_data(num_records)
    print(f"    Generated {len(raw_data['product_id'])} records")
    
    # Process data
    print("\n[2] Processing data...")
    df = process_sales_data(raw_data)
    print(f"    DataFrame shape: {df.shape}")
    
    # Analyze
    print("\n[3] Running analysis...")
    analyzer = SalesAnalyzer(df)
    
    print("\n--- Summary ---")
    print(analyzer.get_summary())
    
    print("\n--- Top 5 Products ---")
    print(analyzer.top_products(5))
    
    print("\n--- Category Performance ---")
    print(analyzer.category_performance())
    
    return df, analyzer


def run_visualization(df):
    """Generate visualizations."""
    print("\n" + "=" * 60)
    print("Generating Visualizations")
    print("=" * 60)
    
    try:
        from src.visualizer import SalesVisualizer
        
        viz = SalesVisualizer(df)
        saved_files = viz.generate_dashboard('outputs/charts')
        
        print(f"\nGenerated {len(saved_files)} charts")
        return saved_files
    except ImportError as e:
        print(f"Visualization requires matplotlib and seaborn: {e}")
        print("Install with: pip install matplotlib seaborn")
        return []


def run_database_operations(df):
    """Store data in SQLite database."""
    print("\n" + "=" * 60)
    print("Database Operations")
    print("=" * 60)
    
    from src.database import SalesDatabase
    
    db = SalesDatabase('data/sales.db')
    
    # Clear and insert fresh data
    db.clear_all_data()
    db.insert_sales_data(df)
    
    # Show some queries
    print("\n--- Revenue by Category (SQL) ---")
    print(db.get_revenue_by_category())
    
    print("\n--- Top 5 Products (SQL) ---")
    print(db.get_top_products(5))
    
    print("\n--- Database Stats ---")
    stats = db.get_stats()
    print(f"    Total records: {stats['total_records']}")
    print(f"    Total revenue: ${stats['total_revenue']:,.2f}")
    
    return db


def run_report_generation(df, analyzer):
    """Generate reports in multiple formats."""
    print("\n" + "=" * 60)
    print("Generating Reports")
    print("=" * 60)
    
    from src.report_generator import ReportGenerator
    
    report_gen = ReportGenerator(df, analyzer)
    
    # HTML Report
    html_path = report_gen.generate_html_report('outputs/reports/sales_report.html')
    
    # Markdown Report
    md_path = report_gen.generate_markdown_report('outputs/reports/sales_report.md')
    
    # Excel Report
    try:
        excel_path = report_gen.generate_excel_report('outputs/reports/sales_report.xlsx')
    except ImportError:
        print("    Excel export skipped (install openpyxl)")
        excel_path = None
    
    return {'html': html_path, 'markdown': md_path, 'excel': excel_path}


def run_full_pipeline(num_records=1000):
    """Run complete analysis pipeline."""
    print("\n" + "=" * 60)
    print("FULL ANALYSIS PIPELINE")
    print("=" * 60)
    
    # Create output directories
    Path('outputs/charts').mkdir(parents=True, exist_ok=True)
    Path('outputs/reports').mkdir(parents=True, exist_ok=True)
    Path('data').mkdir(parents=True, exist_ok=True)
    
    # Step 1: Basic analysis
    df, analyzer = run_basic_analysis(num_records)
    
    # Step 2: Visualizations
    run_visualization(df)
    
    # Step 3: Database
    run_database_operations(df)
    
    # Step 4: Reports
    run_report_generation(df, analyzer)
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE!")
    print("=" * 60)
    print("\nOutputs generated:")
    print("  - Charts: outputs/charts/")
    print("  - Reports: outputs/reports/")
    print("  - Database: data/sales.db")
    print("\nTo run interactive dashboard:")
    print("  streamlit run src/dashboard.py")


def main():
    """Main entry point with CLI arguments."""
    parser = argparse.ArgumentParser(description='Sales Data Analyzer')
    parser.add_argument('--records', type=int, default=1000,
                        help='Number of records to generate (default: 1000)')
    parser.add_argument('--mode', choices=['basic', 'full', 'viz', 'db', 'report'],
                        default='full', help='Analysis mode')
    
    args = parser.parse_args()
    
    if args.mode == 'basic':
        run_basic_analysis(args.records)
    elif args.mode == 'viz':
        df, _ = run_basic_analysis(args.records)
        run_visualization(df)
    elif args.mode == 'db':
        df, _ = run_basic_analysis(args.records)
        run_database_operations(df)
    elif args.mode == 'report':
        df, analyzer = run_basic_analysis(args.records)
        run_report_generation(df, analyzer)
    else:
        run_full_pipeline(args.records)


if __name__ == "__main__":
    main()
