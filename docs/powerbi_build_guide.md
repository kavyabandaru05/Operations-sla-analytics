# Power BI Build Guide: Operations SLA Analytics
File: data/tickets_clean.csv (6,655 rows). Time: about 25 minutes.

## Step 1: Load
Home → Get data → Text/CSV → tickets_clean.csv → Transform Data. Set types:
- `created_at`, `first_response_at`, `resolved_at` → **Date/Time**
- `sla_target_hours`, `reopened`, `sla_breached` → **Whole Number**
- `resolution_hours`, `first_response_hours`, `csat_score` → **Decimal Number**
- `created_date` → **Date**; rest Text
Close & Apply. Rename the table to `tickets`.

## Step 2: Measures (Home → New measure)
```DAX
Total Tickets = COUNTROWS(tickets)
Breached Tickets = SUM(tickets[sla_breached])
SLA Breach % = DIVIDE([Breached Tickets], [Total Tickets])
Avg Resolution Hrs = AVERAGE(tickets[resolution_hours])
Avg First Response Hrs = AVERAGE(tickets[first_response_hours])
Reopen % = DIVIDE(SUM(tickets[reopened]), [Total Tickets])
Avg CSAT = AVERAGE(tickets[csat_score])
Backlog = CALCULATE([Total Tickets], tickets[status] IN {"Open","In Progress"})
Share of Breaches = DIVIDE([Breached Tickets], CALCULATE([Breached Tickets], ALL(tickets)))
```
Format the three % measures as Percentage. Check with no filters: Total Tickets **6,655**, SLA Breach % **36.1%**, Avg Resolution Hrs **28.25**, Backlog **146**.

## Step 3: Page 1 "SLA Overview"
| Visual | Fields |
|---|---|
| 6 Cards | Total Tickets, SLA Breach %, Avg Resolution Hrs, Avg First Response Hrs, Avg CSAT, Backlog |
| Line and column chart | X: `created_month`; columns: Total Tickets; line: SLA Breach % |
| Bar chart | Y: `team`; X: SLA Breach % (sort descending) |
| Clustered column | X: `priority`; Y: Avg Resolution Hrs, plus `sla_target_hours` (Average) to compare with target |
| Pareto-style bar | Y: `root_cause`; X: Breached Tickets (sort descending) |
| Column chart | X: `weekday`; Y: Total Tickets |
| Slicers (dropdown) | `created_month`, `team`, `priority`, `channel`, `customer_tier` |

Add a visual-level filter `team` is not "Unassigned" on the team chart.
Tip: put priority in order Critical, High, Medium, Low by sorting by `sla_target_hours` (Column tools → Sort by column).

## Step 4: Page 2 "Executive Summary" (text box)
- **Logistics, Billing and Technical Support breach 55%, 48%, 43%** of tickets (Account Access 9%). Action: add capacity or triage rules there.
- **Technical Support and Billing cause about 75% of all breaches.** Action: fix process and staffing before individual root causes.
- **Breached tickets score CSAT 3.24 vs 4.07 on time.** Action: treat SLA as a customer-experience KPI; clear the 146-ticket backlog first.
- Note: "Simulated data. SLA uses calendar hours."

## Step 5: Check and save
Clear slicers, confirm the numbers in Step 2, take a screenshot as validation evidence, then save as `SLA_Analytics_Dashboard.pbix` and put it with screenshots in `dashboard/`.
