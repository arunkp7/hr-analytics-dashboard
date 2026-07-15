import pandas as pd
from sqlalchemy import create_engine, text

# ── YOUR POSTGRESQL PASSWORD ──
PASSWORD = "postgres123"
# ─────────────────────────────

engine = create_engine(
    f'postgresql://postgres:{PASSWORD}@localhost:5432/hr_analytics_db'
)

# ── UPDATE THIS PATH to where your CSV file is ──
df = pd.read_csv(r'C:\Users\ARUN\Desktop\hr-analytics\data\hr_employee_cleaned.csv')

# Clean column names — lowercase and replace spaces with underscores
df.columns = df.columns.str.lower().str.replace(' ', '_')

print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
print(f"Columns: {list(df.columns)}")

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE hr_employees RESTART IDENTITY;"))

df.to_sql(
    "hr_employees",
    engine,
    if_exists="append",
    index=False
)
print(f"\n✓ Successfully loaded {len(df)} rows into hr_employees!")
print(f"\n✓ Successfully loaded {len(df)} rows into hr_employees!")