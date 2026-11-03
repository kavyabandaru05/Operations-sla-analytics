# Requirements: Operations SLA Analytics

## 1. Stakeholder and decision
- **Primary stakeholder:** Head of Customer Operations / Support Team Leads
- **Decisions enabled:** where to add staff or training, which root causes to fix at source, whether SLA targets are realistic
- **Measurable benefit:** lower SLA breach rate and shorter resolution time on the worst teams; visibility of backlog

## 2. Scope
**In scope:** Jul-Dec 2025 tickets; volume, resolution time, first-response time, SLA breaches, reopen rate, CSAT, root causes
**Out of scope:** agent-level performance ranking, business-hours calendars, cost per ticket, forecasting

## 3. KPI definitions
| KPI | Definition |
|---|---|
| SLA target (hours) | Critical 4, High 8, Medium 24, Low 72 (calendar hours) |
| Resolution hours | resolved_at - created_at (resolved tickets only) |
| SLA breached | Resolved ticket: resolution hours > target. Open ticket: age at 31-Dec-2025 > target |
| SLA breach % | Breached tickets / all tickets |
| First response hours | first_response_at - created_at |
| Reopen % | Reopened tickets / all tickets |
| Avg CSAT | Mean of csat_score (1-5; about 55% of resolved tickets are rated) |
| Backlog | Tickets with status Open or In Progress at 31-Dec-2025 |
| Share of breaches | Breaches for a root cause / all breaches |

## 4. Inputs and outputs
- **Input:** data/tickets_raw.csv (14 columns, simulated)
- **Outputs:** data/tickets_clean.csv, docs/validation_log.csv, dashboard/kpi_*.csv, interactive dashboard, executive summary

## 5. Dashboard requirements
- Filters: month, team, priority, channel, customer tier
- Visuals: KPI cards, monthly volume + breach % trend, breach % by team, priority vs SLA target, root-cause Pareto, weekday volume, CSAT breached vs not
- Executive summary page with 3 insights and recommended actions

## 6. Acceptance criteria
- [ ] KPIs traceable to sql/kpi_queries.sql
- [ ] Validation log lists every check, rows affected and action
- [ ] Dashboard totals reconcile: 6,656 tickets, breach % 36.09, avg resolution 29.16 h
- [ ] Filters work and update every visual
- [ ] README reproduces everything from the raw file; limitations documented

## 7. Assumptions
- Data is simulated; findings illustrate the method, not a real business
- SLA clock uses calendar hours, not business hours
- Tickets still open at 31-Dec-2025 count as breached only if already past target
