
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = BASE_DIR / "data" / "tickets_clean.csv"
DB_PATH = BASE_DIR / "data" / "sla_analytics.db"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)

tests = []

def check(name, condition, details):
    tests.append({
        "test_name": name,
        "result": "PASS" if condition else "FAIL",
        "details": details
    })

# Load cleaned data
df = pd.read_csv(CSV_PATH)

# Test 1: Dataset is not empty
check(
    "Dataset not empty",
    len(df) > 0,
    f"Rows found: {len(df)}"
)

# Test 2: Unique ticket IDs
check(
    "Unique ticket IDs",
    df["ticket_id"].is_unique,
    f"Duplicate IDs: {df['ticket_id'].duplicated().sum()}"
)

# Test 3: No duplicate rows
check(
    "No duplicate records",
    df.duplicated().sum() == 0,
    f"Duplicate rows: {df.duplicated().sum()}"
)

# Test 4: Required columns exist
required_columns = [
    "ticket_id", "created_at", "priority", "status",
    "sla_target_hours", "resolution_hours",
    "first_response_hours", "sla_breached",
    "csat_score", "reopened"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

check(
    "Required columns present",
    len(missing_columns) == 0,
    f"Missing columns: {missing_columns}"
)

# Test 5: SLA breach flag is binary
check(
    "Valid SLA breach flags",
    df["sla_breached"].isin([0, 1]).all(),
    "SLA breach values must be 0 or 1"
)

# Test 6: Reopened flag is binary
check(
    "Valid reopened flags",
    df["reopened"].isin([0, 1]).all(),
    "Reopened values must be 0 or 1"
)

# Test 7: SLA targets are positive
check(
    "Positive SLA targets",
    (df["sla_target_hours"] > 0).all(),
    "All SLA targets must be greater than zero"
)

# Test 8: Valid CSAT range
valid_csat = df["csat_score"].dropna().between(1, 5).all()

check(
    "CSAT within 1-5",
    valid_csat,
    "Non-missing CSAT scores must be between 1 and 5"
)

# Test 9: First response cannot precede creation
created = pd.to_datetime(df["created_at"], errors="coerce")
response = pd.to_datetime(df["first_response_at"], errors="coerce")

check(
    "Valid response timestamps",
    (response >= created).all(),
    "First response must not precede ticket creation"
)

# Test 10: Database and CSV row counts match
with sqlite3.connect(DB_PATH) as conn:
    db_count = pd.read_sql_query(
        "SELECT COUNT(*) AS total FROM tickets", conn
    ).iloc[0, 0]

check(
    "CSV and SQLite row counts match",
    len(df) == db_count,
    f"CSV: {len(df)}, SQLite: {db_count}"
)

# Export test results
results = pd.DataFrame(tests)
results.to_csv(
    REPORT_DIR / "data_quality_test_results.csv",
    index=False
)

print("\nDATA QUALITY TEST REPORT")
print("=" * 45)
print(results.to_string(index=False))

passed = (results["result"] == "PASS").sum()
failed = (results["result"] == "FAIL").sum()

print("\nTotal tests:", len(results))
print("Passed:", passed)
print("Failed:", failed)

print("\nReport saved in reports/data_quality_test_results.csv")

if failed:
    raise SystemExit("Some data quality tests failed.")
else:
    print("\nAll data quality tests passed!")
