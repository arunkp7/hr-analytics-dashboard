# HR Analytics Dashboard — Employee Attrition Analysis

End-to-end HR analytics project analyzing employee attrition patterns 
using the IBM HR Analytics dataset across Excel, SQL, Python, and Power BI.

## Tech Stack
- **Excel** — Data cleaning, pivot tables, KPI calculations
- **PostgreSQL** — 10 analytical SQL queries
- **Python** — EDA, correlation analysis, visualizations
- **Power BI** — 5-page interactive dashboard with DAX

## Dataset
IBM HR Analytics Employee Attrition Dataset
- 1,470 employees · 35 features · Available on Kaggle

## Key Business Insights
- Overall attrition rate: 16.1% (above 10% industry benchmark)
- Sales department has highest attrition at 20.6%
- Overtime workers are 3x more likely to leave (30.5% vs 10.4%)
- Employees who left earned ₹2,046 less on average than those who stayed
- Single employees leave at 25.5% — highest among marital status groups

## Project Structure
hr-analytics/
├── data/
│   └── hr_employee_cleaned.csv
├── sql/
│   └── queries.sql
├── python/
│   └── eda.py
├── outputs/
│   └── (8 EDA charts)
└── HR_Analytics_Dashboard.pbix

## Dashboard Pages
1. **Executive Dashboard** — 6 KPI cards, attrition split, dept & role charts
2. **Attrition Deep Dive** — Age, marital status, travel, education analysis
3. **Salary & Satisfaction** — Income gap, job satisfaction, work life balance
4. **Overtime & Experience** — Overtime impact, tenure, job level analysis
5. **Demographics** — Gender, age distribution, education field, income band

## How to Run
1. Download IBM HR dataset from Kaggle
2. Open `hr_employee_cleaned.csv` in Excel for data cleaning
3. Load to PostgreSQL and run `sql/queries.sql`
4. Run `python python/eda.py` for EDA charts
5. Open `HR_Analytics_Dashboard.pbix` in Power BI Desktop