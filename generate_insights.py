
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DASHBOARD_DIR = BASE_DIR / "dashboard"
OUTPUT_DIR = BASE_DIR / "reports"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load SQL query results
kpi = pd.read_csv(DASHBOARD_DIR / "kpi_result_1.csv")
monthly = pd.read_csv(DASHBOARD_DIR / "kpi_result_2.csv")
priority = pd.read_csv(DASHBOARD_DIR / "kpi_result_3.csv")
team = pd.read_csv(DASHBOARD_DIR / "kpi_result_4.csv")
root_cause = pd.read_csv(DASHBOARD_DIR / "kpi_result_5.csv")
weekday = pd.read_csv(DASHBOARD_DIR / "kpi_result_6.csv")
csat = pd.read_csv(DASHBOARD_DIR / "kpi_result_7.csv")

# Extract headline KPIs
total_tickets = int(kpi.loc[0, "total_tickets"])
breach_rate = kpi.loc[0, "sla_breach_pct"]
avg_resolution = kpi.loc[0, "avg_resolution_hrs"]
avg_response = kpi.loc[0, "avg_first_response_hrs"]
reopen_rate = kpi.loc[0, "reopen_pct"]
avg_csat = kpi.loc[0, "avg_csat"]
backlog = int(kpi.loc[0, "backlog"])

# Identify important patterns
worst_team = team.loc[team["team"] != "Unassigned"].sort_values(
    "breach_pct", ascending=False
).iloc[0]

worst_month = monthly.sort_values(
    "breach_pct", ascending=False
).iloc[0]

worst_priority = priority.sort_values(
    "breach_pct", ascending=False
).iloc[0]

worst_root_cause = root_cause.sort_values(
    "breached_tickets", ascending=False
).iloc[0]

csat_no_breach = csat.loc[csat["sla_breached"] == 0, "avg_csat"].iloc[0]
csat_breach = csat.loc[csat["sla_breached"] == 1, "avg_csat"].iloc[0]

# Build report
report = f"""
OPERATIONS SLA ANALYTICS
AUTOMATED BUSINESS INSIGHTS REPORT
===================================

1. OVERALL PERFORMANCE
----------------------
Total Tickets: {total_tickets}
SLA Breach Rate: {breach_rate}%
Average Resolution Time: {avg_resolution} hours
Average First Response Time: {avg_response} hours
Reopened Ticket Rate: {reopen_rate}%
Average Customer Satisfaction: {avg_csat}/5
Current Backlog: {backlog} tickets

2. TEAM PERFORMANCE
-------------------
Highest SLA Breach Team: {worst_team['team']}
Team Breach Rate: {worst_team['breach_pct']}%

3. MONTHLY PERFORMANCE
----------------------
Worst Month: {worst_month['created_month']}
Monthly Breach Rate: {worst_month['breach_pct']}%

4. PRIORITY ANALYSIS
--------------------
Highest Breach Priority: {worst_priority['priority']}
Priority Breach Rate: {worst_priority['breach_pct']}%

5. ROOT CAUSE ANALYSIS
---------------------
Root Cause with Most Breaches: {worst_root_cause['root_cause']}
Breached Tickets: {int(worst_root_cause['breached_tickets'])}

6. CUSTOMER SATISFACTION
------------------------
Average CSAT Without SLA Breach: {csat_no_breach}/5
Average CSAT With SLA Breach: {csat_breach}/5

7. RECOMMENDATIONS
------------------
- Investigate the team with the highest SLA breach rate.
- Review staffing and workload during the worst-performing month.
- Examine the root causes contributing most to SLA breaches.
- Prioritise breached tickets to improve customer satisfaction.
- Monitor backlog and resolution time regularly.

Note: This report is generated from the SQL KPI result files.
The dataset is synthetic and the findings represent this dataset.
"""

# Save report
report_path = OUTPUT_DIR / "automated_insights_report.txt"
report_path.write_text(report, encoding="utf-8")

print(report)
print("\nInsights report saved to:", report_path)
