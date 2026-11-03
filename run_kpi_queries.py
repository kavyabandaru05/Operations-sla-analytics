import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

db_path = BASE_DIR / "data" / "sla_analytics.db"
sql_path = BASE_DIR / "sql" / "kpi_queries.sql"
output_dir = BASE_DIR / "dashboard"

output_dir.mkdir(exist_ok=True)

sql_text = sql_path.read_text(encoding="utf-8")

queries = []

for chunk in sql_text.split(";"):
    # Remove SQL comment-only lines
    lines = [
        line for line in chunk.splitlines()
        if not line.strip().startswith("--")
    ]

    query = "\n".join(lines).strip()

    if query:
        queries.append(query)

conn = sqlite3.connect(db_path)

for i, query in enumerate(queries, start=1):
    result = pd.read_sql_query(query, conn)

    filename = output_dir / f"kpi_result_{i}.csv"
    result.to_csv(filename, index=False)

    print(f"\nQuery {i} executed successfully")
    print(result.to_string(index=False))

conn.close()

print(f"\nCompleted: {len(queries)} SQL queries.")