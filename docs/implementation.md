# Operations SLA Analytics – Implementation Documentation

## 1. Project Overview

This project analyzes support ticket operations to measure SLA compliance, resolution efficiency, ticket backlog, root causes and customer satisfaction.

The implementation uses Python for data processing, SQLite for analytical queries and Power BI for dashboard reporting.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Data processing and automation |
| Pandas | Data cleaning and analysis |
| SQLite | Database storage |
| SQL | KPI calculations |
| Power BI | Interactive visualization |
| VS Code | Development environment |
| Git and GitHub | Version control |

## 3. Project Architecture

The project follows this processing workflow:

1. Raw ticket data is stored in `data/tickets_raw.csv`.
2. Python cleaning script validates and transforms the raw data.
3. Cleaned records are exported to `data/tickets_clean.csv`.
4. Validation results are stored in `docs/validation_log.csv`.
5. Cleaned data is loaded into SQLite using `load_to_sqlite.py`.
6. SQL queries calculate operational KPIs.
7. Query results are exported as CSV files into `dashboard/`.
8. Python generates automated business insights.
9. Data-quality tests verify the dataset and database.
10. Power BI uses the cleaned data for interactive reporting.

## 4. Data Cleaning and Validation

Implementation file: `clean_and_validate.py`

The following checks are performed:

- Standardisation of text fields.
- Removal of exact duplicate records.
- Removal of records with missing priority.
- Replacement of missing team values with `Unassigned`.
- Validation of priority and status categories.
- Timestamp parsing and validation.
- Removal of invalid response and resolution timestamps.
- Validation of SLA target values.
- CSAT validation against the 1–5 scale.
- Reopened flag validation.
- Identification of extreme resolution durations.

The cleaning process also calculates:

- Resolution hours.
- First response hours.
- SLA measurement hours.
- SLA breach flag.
- Creation month.
- Creation date.
- Weekday.

## 5. SLA Calculation Logic

The project uses calendar hours rather than business hours.

SLA targets:

| Priority | SLA Target |
|---|---:|
| Critical | 4 hours |
| High | 8 hours |
| Medium | 24 hours |
| Low | 72 hours |

For resolved tickets, resolution duration is compared with the SLA target.

For unresolved tickets, ticket age is calculated using the fixed snapshot:

`2025-12-31 23:59:59`

A ticket is considered breached when its SLA measurement exceeds its target.

## 6. Database Implementation

Implementation file: `load_to_sqlite.py`

Database location:

`data/sla_analytics.db`

Database table:

`tickets`

The cleaned CSV is loaded into SQLite using Pandas `to_sql()`.

The database was verified to contain 6,656 ticket records and 22 columns.

## 7. SQL Analysis

SQL file: `sql/kpi_queries.sql`

Seven analytical queries were implemented:

1. Headline operational KPIs.
2. Monthly ticket volume and SLA breach trends.
3. Priority-wise SLA performance.
4. Team-wise operational performance.
5. Root-cause analysis.
6. Weekday and channel analysis.
7. SLA breach and customer satisfaction comparison.

Execution file:

`run_kpi_queries.py`

Each query result is exported as a separate CSV file in the dashboard directory.

## 8. Automated Business Insights

Implementation file: `generate_insights.py`

The Python script reads the SQL-generated CSV files and produces an automated report.

Output:

`reports/automated_insights_report.txt`

The report identifies:

- Overall SLA performance.
- Team with the highest breach rate.
- Worst-performing month.
- Priority with the highest breach rate.
- Root cause with the most breaches.
- CSAT differences between breached and non-breached tickets.
- Recommended operational actions.

## 9. Data Quality Testing

Implementation file: `test_data_quality.py`

Ten automated checks were performed:

1. Dataset is not empty.
2. Ticket IDs are unique.
3. No duplicate records exist.
4. Required columns are present.
5. SLA breach flags are binary.
6. Reopened flags are binary.
7. SLA targets are positive.
8. CSAT values are within the valid range.
9. First response timestamps do not precede ticket creation.
10. CSV and SQLite row counts match.

Latest test results:

- Total tests: 10
- Passed: 10
- Failed: 0

Test evidence:

`reports/data_quality_test_results.csv`

## 10. Execution Instructions

Run the following commands from the project root directory, in order:

```powershell
py clean_and_validate.py
py load_to_sqlite.py
py run_kpi_queries.py
py generate_insights.py
py test_data_quality.py
```

## 11. Current Analytical Results

| KPI | Result |
|---|---:|
| Total tickets | 6,656 |
| SLA breach rate | 36.09% |
| Average resolution time | 29.16 hours |
| Average first response time | 3.78 hours |
| Reopened ticket rate | 5.86% |
| Average CSAT | 3.77 / 5 |
| Backlog | 146 |

## 12. Limitations

- The dataset is synthetic.
- SLA calculations use calendar hours.
- No business-hours or holiday calendar is implemented.
- No real-time ticket monitoring is available.
- No production support-system integration is included.
- Historical analysis does not establish causation.

## 13. Future Improvements

- Integrate with a real ticket management system.
- Add business-hours SLA calculations.
- Develop automated SLA breach alerts.
- Introduce predictive ticket-volume analysis.
- Add agent workload and capacity analysis.
- Implement scheduled data refreshes.
- Improve production monitoring and access controls.

## 14. Conclusion

The project demonstrates an end-to-end operations analytics workflow using Python, SQL, SQLite and Power BI. It transforms raw ticket records into validated data, measurable KPIs and actionable business insights.