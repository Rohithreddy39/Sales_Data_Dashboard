# Sales Data Analyzer - Extended Edition

A comprehensive Python project covering **NumPy**, **Pandas**, **Visualization**, **Database**, and **Reporting**.

## Project Structure

```
sales_analyzer/
├── main.py                     # Entry point with CLI
├── requirements.txt            # Dependencies
├── src/
│   ├── __init__.py
│   ├── data_generator.py       # NumPy fundamentals
│   ├── data_processor.py       # Pandas fundamentals
│   ├── analyzer.py             # Analysis & statistics
│   ├── visualizer.py           # Matplotlib & Seaborn
│   ├── database.py             # SQLite integration
│   ├── report_generator.py     # HTML/Markdown/Excel reports
│   └── dashboard.py            # Streamlit interactive app
├── data/                       # Database files
├── outputs/
│   ├── charts/                 # Generated visualizations
│   └── reports/                # Generated reports
└── README.md
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run full pipeline
python main.py

# Run specific mode
python main.py --mode basic      # Just analysis
python main.py --mode viz        # + visualizations
python main.py --mode db         # + database
python main.py --mode report     # + reports

# Custom record count
python main.py --records 5000

# Interactive dashboard
streamlit run src/dashboard.py
```

## Learning Modules

### 1. NumPy (`data_generator.py`)

| Concept | Description |
|---------|-------------|
| Array creation | `np.array`, `np.zeros`, `np.arange`, `np.linspace` |
| Random generation | `np.random.randint`, `np.random.normal`, `np.random.choice` |
| Vectorization | Element-wise operations without loops |
| Broadcasting | Operations on different-shaped arrays |
| Statistics | `np.mean`, `np.std`, `np.percentile`, `np.sum` |
| Conditionals | `np.where`, `np.select`, `np.clip` |

### 2. Pandas (`data_processor.py`)

| Concept | Description |
|---------|-------------|
| DataFrame | Creating, inspecting, info |
| Data types | `astype`, categorical, datetime |
| Selection | `[]`, `.loc`, `.iloc` |
| Filtering | Boolean indexing, multiple conditions |
| Transformation | `apply`, `map`, feature engineering |
| Aggregation | `groupby`, `agg`, `pivot_table` |
| Merging | `merge`, `join`, `concat` |
| Cleaning | `fillna`, `drop_duplicates`, validation |

### 3. Analysis (`analyzer.py`)

| Concept | Description |
|---------|-------------|
| OOP | Class-based design with Pandas |
| Statistics | Summary stats, percentiles, outliers |
| Correlation | Correlation matrix analysis |
| Time series | Monthly trends, day-of-week patterns |
| Segmentation | Cohort analysis, customer tiers |

### 4. Visualization (`visualizer.py`)

| Chart Type | Use Case |
|------------|----------|
| Bar charts | Category comparisons |
| Line charts | Trends over time |
| Histograms | Distribution analysis |
| Box plots | Statistical distribution |
| Pie charts | Part-to-whole relationships |
| Heatmaps | Correlation matrices |
| Scatter plots | Relationship analysis |

### 5. Database (`database.py`)

| Concept | Description |
|---------|-------------|
| Connection | Context managers, SQLite |
| CRUD | Insert, select, update, delete |
| SQL queries | Aggregation, joins, subqueries |
| Pandas integration | `read_sql`, `to_sql` |
| Optimization | Indexes, summary tables |

### 6. Dashboard (`dashboard.py`)

| Feature | Description |
|---------|-------------|
| Streamlit | Interactive web app |
| Widgets | Sliders, selectors, date pickers |
| Caching | `@st.cache_data` for performance |
| Layouts | Columns, tabs, containers |
| Export | Download CSV/reports |

### 7. Reporting (`report_generator.py`)

| Format | Features |
|--------|----------|
| HTML | Styled report with CSS |
| Markdown | GitHub-compatible documentation |
| Excel | Multi-sheet workbooks |

## Skills Progression

```
Level 1: Basics
├── NumPy arrays and operations
├── Pandas DataFrames
└── Basic analysis

Level 2: Intermediate
├── Data visualization
├── Statistical analysis
└── Data cleaning

Level 3: Advanced
├── Database integration
├── Interactive dashboards
├── Automated reporting
└── CLI applications
```

## Exercises

### Beginner
1. Generate 500 records and find the top 3 categories
2. Filter sales above $500 in the "North" region
3. Calculate average discount per region

### Intermediate
1. Add a new column for profit margin
2. Create a pivot table: month × category → revenue
3. Find products with consistently high sales

### Advanced
1. Build a recommendation system for products
2. Implement time-series forecasting
3. Add user authentication to the dashboard
4. Deploy to cloud (Heroku/Streamlit Cloud)

## Extending Further

Ideas for continued learning:

- **Machine Learning**: Add scikit-learn for predictions
- **API**: Create REST API with FastAPI
- **Cloud**: Deploy to AWS/GCP
- **Testing**: Add pytest unit tests
- **CI/CD**: GitHub Actions workflow
- **Docker**: Containerize the application
Testing the git pull
## Resources

- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [Seaborn Documentation](https://seaborn.pydata.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLite Documentation](https://sqlite.org/docs.html)
