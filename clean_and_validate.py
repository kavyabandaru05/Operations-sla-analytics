
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. PROJECT PATHS AND REPORTING SNAPSHOT
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

RAW_FILE = BASE_DIR / "data" / "tickets_raw.csv"
CLEAN_FILE = BASE_DIR / "data" / "tickets_clean.csv"
LOG_FILE = BASE_DIR / "docs" / "validation_log.csv"

SNAPSHOT = pd.Timestamp("2025-12-31 23:59:59")

log = []

def record_check(name, count, action):
    log.append({
        "check": name,
        "rows_affected": int(count),
        "action": action
    })

# --------------------------------------------------
# 2. LOAD RAW DATA
# --------------------------------------------------

raw = pd.read_csv(RAW_FILE)
df = raw.copy()

record_check("Total raw rows", len(df), "Baseline")

required_columns = [
    "ticket_id", "created_at", "first_response_at",
    "resolved_at", "team", "agent_id", "priority",
    "sla_target_hours", "root_cause", "channel",
    "customer_tier", "status", "reopened", "csat_score"
]

missing_columns = set(required_columns) - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# --------------------------------------------------
# 3. STANDARDISE TEXT FIELDS
# --------------------------------------------------

text_columns = [
    "ticket_id", "team", "agent_id", "priority",
    "root_cause", "channel", "customer_tier", "status"
]

for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

# Convert empty strings into missing values
for col in text_columns:
    df[col] = df[col].replace("", pd.NA)

# Standardise priority and status
original_priority = df["priority"].copy()

df["priority"] = df["priority"].str.title()
df["status"] = df["status"].str.title()

changed_priority = (
    original_priority.notna()
    & (original_priority != df["priority"])
).sum()

record_check(
    "Priority standardisation",
    changed_priority,
    "Trimmed whitespace and standardised casing"
)

# --------------------------------------------------
# 4. DUPLICATE VALIDATION
# --------------------------------------------------

duplicates = df.duplicated().sum()

record_check(
    "Exact duplicate rows",
    duplicates,
    "Removed"
)

df = df.drop_duplicates().copy()

# --------------------------------------------------
# 5. MISSING PRIORITY AND TEAM
# --------------------------------------------------

missing_priority = df["priority"].isna()

record_check(
    "Missing priority",
    missing_priority.sum(),
    "Removed because SLA category cannot be determined"
)

df = df.loc[~missing_priority].copy()

missing_team = df["team"].isna().sum()

record_check(
    "Missing team",
    missing_team,
    "Replaced with Unassigned"
)

df["team"] = df["team"].fillna("Unassigned")

# --------------------------------------------------
# 6. VALIDATE PRIORITY AND STATUS
# --------------------------------------------------

valid_priorities = ["Critical", "High", "Medium", "Low"]

invalid_priority = ~df["priority"].isin(valid_priorities)

record_check(
    "Invalid priority values",
    invalid_priority.sum(),
    "Removed"
)

df = df.loc[~invalid_priority].copy()

valid_statuses = ["Closed", "Resolved", "Open", "In Progress"]

invalid_status = ~df["status"].isin(valid_statuses)

record_check(
    "Invalid ticket statuses",
    invalid_status.sum(),
    "Removed"
)

df = df.loc[~invalid_status].copy()

# --------------------------------------------------
# 7. DATE VALIDATION
# --------------------------------------------------

date_columns = [
    "created_at",
    "first_response_at",
    "resolved_at"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

invalid_created = df["created_at"].isna()

record_check(
    "Invalid or missing creation timestamps",
    invalid_created.sum(),
    "Removed"
)

df = df.loc[~invalid_created].copy()

invalid_response = df["first_response_at"].isna()

record_check(
    "Invalid or missing first response timestamps",
    invalid_response.sum(),
    "Removed"
)

df = df.loc[~invalid_response].copy()

response_before_creation = (
    df["first_response_at"] < df["created_at"]
)

record_check(
    "First response before ticket creation",
    response_before_creation.sum(),
    "Removed"
)

df = df.loc[~response_before_creation].copy()

resolved_statuses = ["Closed", "Resolved"]

missing_resolution = (
    df["status"].isin(resolved_statuses)
    & df["resolved_at"].isna()
)

record_check(
    "Closed/Resolved tickets without resolution timestamp",
    missing_resolution.sum(),
    "Removed"
)

df = df.loc[~missing_resolution].copy()

resolution_before_creation = (
    df["resolved_at"].notna()
    & (df["resolved_at"] < df["created_at"])
)

record_check(
    "Resolution before ticket creation",
    resolution_before_creation.sum(),
    "Removed"
)

df = df.loc[~resolution_before_creation].copy()

# --------------------------------------------------
# 8. SLA TARGET VALIDATION
# --------------------------------------------------

df["sla_target_hours"] = pd.to_numeric(
    df["sla_target_hours"], errors="coerce"
)

invalid_sla = (
    df["sla_target_hours"].isna()
    | (df["sla_target_hours"] <= 0)
)

record_check(
    "Missing or non-positive SLA targets",
    invalid_sla.sum(),
    "Removed"
)

df = df.loc[~invalid_sla].copy()

# Verify expected SLA targets by priority
expected_sla = {
    "Critical": 4,
    "High": 8,
    "Medium": 24,
    "Low": 72
}

expected_values = df["priority"].map(expected_sla)

mismatched_sla = (
    df["sla_target_hours"] != expected_values
)

record_check(
    "SLA target inconsistent with priority",
    mismatched_sla.sum(),
    "Removed for reliable priority-based SLA analysis"
)

df = df.loc[~mismatched_sla].copy()

# --------------------------------------------------
# 9. CSAT VALIDATION
# --------------------------------------------------

df["csat_score"] = pd.to_numeric(
    df["csat_score"], errors="coerce"
)

invalid_csat = (
    df["csat_score"].notna()
    & ~df["csat_score"].between(1, 5)
)

record_check(
    "CSAT outside valid 1-5 range",
    invalid_csat.sum(),
    "Set to missing"
)

df.loc[invalid_csat, "csat_score"] = pd.NA

# --------------------------------------------------
# 10. REOPENED FLAG VALIDATION
# --------------------------------------------------

df["reopened"] = pd.to_numeric(
    df["reopened"], errors="coerce"
)

invalid_reopened = ~df["reopened"].isin([0, 1])

record_check(
    "Invalid reopened flags",
    invalid_reopened.sum(),
    "Removed"
)

df = df.loc[~invalid_reopened].copy()
df["reopened"] = df["reopened"].astype(int)

# --------------------------------------------------
# 11. RESOLUTION AND RESPONSE TIME
# --------------------------------------------------

df["resolution_hours"] = (
    (df["resolved_at"] - df["created_at"])
    .dt.total_seconds() / 3600
).round(2)

df["first_response_hours"] = (
    (df["first_response_at"] - df["created_at"])
    .dt.total_seconds() / 3600
).round(2)

# Flag unusually long resolution times.
# Preserve them unless separately investigated.
df["extreme_resolution_flag"] = (
    df["resolution_hours"] > 2000
).astype(int)

record_check(
    "Extreme resolution times above 2000 hours",
    df["extreme_resolution_flag"].sum(),
    "Flagged for review; not automatically removed"
)

# --------------------------------------------------
# 12. SLA BREACH CALCULATION
# --------------------------------------------------

ticket_age_hours = (
    (SNAPSHOT - df["created_at"])
    .dt.total_seconds() / 3600
).clip(lower=0)

# Resolved tickets use actual resolution time.
# Open and In Progress tickets use age at snapshot.
df["sla_measure_hours"] = df["resolution_hours"].where(
    df["resolved_at"].notna(),
    ticket_age_hours
)

df["sla_breached"] = (
    df["sla_measure_hours"] > df["sla_target_hours"]
).astype(int)

df["created_month"] = df["created_at"].dt.strftime("%Y-%m")
df["created_date"] = df["created_at"].dt.date
df["weekday"] = df["created_at"].dt.day_name()

# --------------------------------------------------
# 13. FINAL VALIDATION AND EXPORT
# --------------------------------------------------

record_check(
    "Rows after cleaning",
    len(df),
    "Final cleaned dataset"
)

CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(CLEAN_FILE, index=False)
pd.DataFrame(log).to_csv(LOG_FILE, index=False)

# --------------------------------------------------
# 14. SUMMARY REPORT
# --------------------------------------------------

print("\n========== DATA CLEANING SUMMARY ==========")

print("Raw rows:", len(raw))
print("Clean rows:", len(df))
print("Rows removed:", len(raw) - len(df))

print("\nValidation log:")
print(pd.DataFrame(log).to_string(index=False))

print("\n========== SLA ANALYSIS ==========")

print(
    "Overall SLA breach rate:",
    round(df["sla_breached"].mean() * 100, 2), "%"
)

print("\nSLA breach by priority:")
print(
    df.groupby("priority")["sla_breached"]
    .mean().mul(100).round(2)
)

print("\nSLA breach by team:")
print(
    df.groupby("team")["sla_breached"]
    .mean().mul(100).round(2)
)

print("\nTicket status:")
print(df["status"].value_counts())

print("\nClean dataset saved to:", CLEAN_FILE)
print("Validation log saved to:", LOG_FILE)
