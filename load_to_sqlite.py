import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

csv_path = BASE_DIR / "data" / "tickets_clean.csv"
db_path = BASE_DIR / "data" / "sla_analytics.db"

# Load cleaned dataset
df = pd.read_csv(csv_path)

# Connect to SQLite
conn = sqlite3.connect(db_path)

# Create or replace tickets table
df.to_sql("tickets", conn, if_exists="replace", index=False)

# Verify table
count = pd.read_sql_query(
    "SELECT COUNT(*) AS total_tickets FROM tickets",
    conn
)

print("Database created successfully!")
print("Total tickets loaded:", count.iloc[0, 0])
print("Database location:", db_path)

conn.close()