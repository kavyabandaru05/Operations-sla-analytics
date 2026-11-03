
# Operations SLA Analytics

## Arrowstack Technologies – Data Analytics Internship | Task 2

An end-to-end data analytics project designed to monitor ticket operations, evaluate Service Level Agreement (SLA) performance, identify operational bottlenecks, and generate actionable business insights through Python, SQL, and Power BI.

---

## 1. Project Overview

Customer support teams handle tickets across multiple priorities, channels, and operational teams. Delayed responses and resolutions can result in SLA violations and reduced customer satisfaction.

This project analyzes ticket-level operational data to evaluate SLA compliance, monitor ticket resolution performance, identify high-risk teams, and understand the relationship between SLA breaches and customer satisfaction.

The project follows a reproducible analytics workflow covering data cleaning, validation, SQL analysis, KPI generation, automated insights, and interactive dashboard development.

**Note:** The dataset used in this project is simulated and is intended for analytical demonstration.

---

## 2. Business Objectives

- Measure overall SLA compliance and breach rates.
- Analyze ticket volume and resolution trends over time.
- Compare operational performance across teams and priorities.
- Identify major contributors to SLA violations.
- Evaluate customer satisfaction in relation to SLA performance.
- Monitor unresolved tickets and operational backlog.
- Provide data-driven recommendations for improving support operations.

---

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Data processing and automation |
| Pandas | Data cleaning and transformation |
| SQLite | Structured data storage |
| SQL | KPI calculations and analytical queries |
| Power BI Desktop | Interactive dashboard |
| CSV | Data exchange and KPI exports |
| Git and GitHub | Version control and project hosting |
| VS Code | Development environment |

---

## 4. Project Architecture

```text
Raw Ticket Dataset
        |
        v
Python Data Cleaning
        |
        v
Data Validation
        |
        v
Cleaned Ticket Dataset
        |
        +----------------------+
        |                      |
        v                      v
   SQLite Database       CSV Exports
        |                      |
        v                      v
    SQL Analysis         Power BI Dashboard
        |                      |
        v                      v
 Automated Insights     Interactive Reports
        |                      |
        +----------+-----------+
                   |
                   v
             Business Insights
                   |
                   v
             Recommendations
```

---

## 5. Dataset Description

The original dataset contains **6,661 ticket records** and 14 columns.

After cleaning and validation, the final dataset contains:

| Metric | Value |
|---|---:|
| Raw records | 6,661 |
| Cleaned records | 6,656 |
| Removed records | 5 |
| Final columns | 22 |
| Data quality tests passed | 10/10 |

### Important Dataset Fields

| Column | Description |
|---|---|
| ticket_id | Unique ticket identifier |
| created_at | Ticket creation timestamp |
| first_response_at | First response timestamp |
| resolved_at | Ticket resolution timestamp |
| team | Responsible support team |
| agent_id | Assigned support agent |
| priority | Ticket priority |
| sla_target_hours | Expected SLA resolution time |
| root_cause | Ticket's underlying issue |
| channel | Ticket communication channel |
| customer_tier | Customer category |
| status | Current ticket status |
| reopened | Indicates whether the ticket was reopened |
| csat_score | Customer satisfaction score |

Additional calculated fields are generated during data processing, including resolution hours, first response hours, SLA breach indicators, and date-related attributes.

---

## 6. Data Cleaning and Validation

Data preparation was performed using `clean_and_validate.py`.

### Cleaning Operations

- Removed exact duplicate records.
- Standardized priority values.
- Removed records with missing priority.
- Filled missing team values with `Unassigned`.
- Removed invalid timestamps.
- Removed first-response timestamps earlier than ticket creation.
- Removed closed or resolved tickets without resolution timestamps.
- Removed records with resolution timestamps earlier than creation.
- Set invalid CSAT scores outside the 1–5 range to missing.
- Flagged extreme resolution durations exceeding 2,000 hours.

Missing resolution timestamps for unresolved tickets were retained.

### SLA Target Rules

| Priority | SLA Target |
|---|---:|
| Critical | 4 hours |
| High | 8 hours |
| Medium | 24 hours |
| Low | 72 hours |

### Validation Results

The validation process checks:

- Unique ticket identifiers.
- Duplicate records.
- Required columns.
- Valid SLA breach indicators.
- Valid reopened flags.
- Positive SLA targets.
- Valid CSAT scores.
- Valid timestamp sequence.
- CSV and SQLite row-count consistency.

**Result: 10 automated data quality tests passed.**

Validation evidence is available in:

- `docs/validation_log.csv`
- `reports/data_quality_test_results.csv`

---

## 7. Key Performance Indicators (KPIs)

The project calculates the following operational KPIs.

| KPI | Result |
|---|---:|
| Total Tickets | 6,656 |
| SLA Breach Rate | 36.09% |
| Average Resolution Time | 29.16 hours |
| Average First Response Time | 3.78 hours |
| Reopened Ticket Rate | 5.86% |
| Average CSAT | 3.77 / 5 |
| Current Backlog | 146 |

### KPI Definitions

**Total Tickets**

Total number of records in the cleaned dataset.

**SLA Breach Rate**

Percentage of tickets whose resolution duration or unresolved ticket age exceeds the applicable SLA target.

**Average Resolution Time**

Average time taken to resolve tickets, excluding unresolved tickets without a resolution duration.

**Average First Response Time**

Average time between ticket creation and the first response.

**Reopened Ticket Rate**

Percentage of tickets marked as reopened.

**Average CSAT**

Average customer satisfaction score, calculated using available valid scores.

**Current Backlog**

Number of tickets with Open or In Progress status.

---

## 8. SQL Analysis

SQL queries are stored in:

`sql/kpi_queries.sql`

The project includes seven analytical query categories:

1. Headline operational KPIs.
2. Monthly ticket volume and SLA breach trends.
3. Priority-wise SLA performance.
4. Team-wise operational performance.
5. Root-cause analysis.
6. Weekday and communication-channel analysis.
7. SLA breach versus customer satisfaction analysis.

The SQLite database is available at:

`data/sla_analytics.db`

---

## 9. Power BI Dashboard

The interactive dashboard is developed using Power BI Desktop.

**Dashboard file:**

`dashboard/Operations_SLA_Analytics.pbix`

### Dashboard Components

- Total ticket KPI.
- SLA breach percentage.
- Average resolution hours.
- Average first response hours.
- Reopened ticket percentage.
- Average CSAT.
- Current backlog.
- Monthly ticket volume and SLA breach trend.
- Ticket volume by weekday and channel.
- Resolution time versus SLA target by priority.
- SLA breach rate by support team.
- Root-cause analysis.
- Customer satisfaction comparison between breached and non-breached tickets.

The dashboard supports analysis through available filters for:

- Month
- Team
- Priority
- Channel
- Customer tier

---

## 10. Key Business Insights

### Team Performance

- Logistics has the highest SLA breach rate at **55.14%**.
- Billing has an SLA breach rate of **48.05%**.
- Technical Support has an SLA breach rate of **43.17%**.
- Account Access and General Enquiry have comparatively lower breach rates.

### Monthly Performance

- December recorded the highest monthly SLA breach rate at **41.45%**.
- October also showed elevated SLA breaches at **40.44%**.
- Monthly performance analysis can help identify periods requiring additional operational attention.

### Root-Cause Analysis

- Performance issues recorded 522 tickets and 228 SLA breaches.
- Outages recorded 512 tickets and 223 SLA breaches.
- Software bugs recorded 456 tickets and 216 SLA breaches.

### Customer Satisfaction

| SLA Category | Average CSAT |
|---|---:|
| SLA Not Breached | 4.07 |
| SLA Breached | 3.24 |

Tickets with SLA breaches have a lower average CSAT score in this dataset.

This indicates an association between SLA performance and customer satisfaction; it does not establish causation.

---

## 11. Business Recommendations

Based on the analysis:

1. **Improve Logistics Operations:** Investigate workload distribution, ticket assignment, and resolution bottlenecks.
2. **Prioritize High-Risk Teams:** Monitor Logistics, Billing, and Technical Support more closely.
3. **Focus on Recurring Issues:** Investigate performance issues, outages, and software bugs.
4. **Introduce Early-Warning Monitoring:** Identify tickets approaching their SLA deadlines.
5. **Improve Customer Experience:** Monitor CSAT for breached tickets and identify recurring customer complaints.
6. **Review Monthly Trends:** Use historical SLA performance to improve staffing and resource planning.

---

## 12. Automated Insights

The project includes an automated insights script:

`generate_insights.py`

It generates a report containing key operational metrics and analytical findings.

Generated report:

`reports/automated_insights_report.txt`

This reduces repetitive manual analysis and makes the reporting workflow more reproducible.

---

## 13. Data Quality Testing

Automated data quality tests are implemented in:

`test_data_quality.py`

Run the tests using:

```bash
py test_data_quality.py
```

The test process validates the cleaned dataset and exports the results to:

`reports/data_quality_test_results.csv`

**Latest recorded result: 10 tests passed, 0 failed.**

---

## 14. How to Run the Project

### Prerequisites

- Python 3.13 or compatible Python version.
- VS Code or another Python IDE.
- Power BI Desktop (for dashboard viewing).
- Git (optional, for version control).

### Step 1: Clone the Repository

```bash
git clone https://github.com/kavyabandaru05/Operations-sla-analytics.git
```

### Step 2: Navigate to the Project

```bash
cd Operations-sla-analytics
```

### Step 3: Install Dependencies

```bash
py -m pip install pandas
```

### Step 4: Run Data Cleaning

```bash
py clean_and_validate.py
```

### Step 5: Load Data into SQLite

```bash
py load_to_sqlite.py
```

### Step 6: Execute SQL KPI Queries

```bash
py run_kpi_queries.py
```

### Step 7: Generate Automated Insights

```bash
py generate_insights.py
```

### Step 8: Run Data Quality Tests

```bash
py test_data_quality.py
```

### Step 9: Open the Power BI Dashboard

Open:

`dashboard/Operations_SLA_Analytics.pbix`

Refresh the dataset if required.

---

## 15. Project Structure

```text
Operations-sla-analytics/
│
├── data/
│   ├── tickets_raw.csv
│   ├── tickets_clean.csv
│   └── sla_analytics.db
│
├── dashboard/
│   ├── Operations_SLA_Analytics.pbix
│   ├── Operations_SLA_Analytics_Presentation.pptx
│   ├── kpi_headline.csv
│   ├── kpi_monthly.csv
│   ├── kpi_priority.csv
│   ├── kpi_team.csv
│   ├── kpi_weekday.csv
│   ├── kpi_root_cause.csv
│   └── kpi_csat_vs_breach.csv
│
├── docs/
│   ├── requirements.md
│   ├── implementation.md
│   ├── decision_log.md
│   ├── work_log.md
│   ├── validation_log.csv
│   └── powerbi_build_guide.md
│
├── reports/
│   ├── automated_insights_report.txt
│   ├── data_quality_test_results.csv
│   └── executive_summary.md
│
├── sql/
│   └── kpi_queries.sql
│
├── clean_and_validate.py
├── generate_data.py
├── generate_insights.py
├── load_to_sqlite.py
├── run_kpi_queries.py
├── test_data_quality.py
│
├── .gitignore
└── README.md
```

---

## 16. Project Documentation and Deliverables

| File | Description |
|---|---|
| `docs/requirements.md` | Stakeholder requirements, scope, and KPI definitions |
| `docs/implementation.md` | Technical implementation and workflow |
| `docs/decision_log.md` | Key project decisions and trade-offs |
| `docs/work_log.md` | Project activity and progress |
| `docs/validation_log.csv` | Data cleaning and validation evidence |
| `docs/powerbi_build_guide.md` | Dashboard implementation guide |
| `reports/executive_summary.md` | Business findings and recommendations |
| `reports/automated_insights_report.txt` | Generated analytical insights |
| `reports/data_quality_test_results.csv` | Automated testing results |
| `dashboard/Operations_SLA_Analytics.pbix` | Interactive Power BI dashboard |
| `dashboard/Operations_SLA_Analytics_Presentation.pptx` | Final project presentation |

---

## 17. Limitations and Future Improvements

### Current Limitations

- The dataset is simulated and may not represent actual business operations.
- SLA calculations use calendar hours rather than business hours.
- Unresolved ticket ages are calculated using a fixed snapshot timestamp.
- Missing CSAT scores are excluded from average CSAT calculations.
- The analysis identifies associations and patterns but does not establish causal relationships.

### Future Improvements

- Integrate real-time ticketing system data.
- Implement automated SLA alerts.
- Add business-hour and holiday-aware SLA calculations.
- Develop predictive models to identify tickets at risk of SLA breaches.
- Introduce role-based dashboards for managers and support agents.
- Automate scheduled reporting and dashboard refreshes.
- Deploy the analytics pipeline to a cloud environment.

---

## 18. Conclusion

The Operations SLA Analytics project demonstrates an end-to-end data analytics workflow using Python, SQL, SQLite, and Power BI.

It transforms raw ticket data into validated analytical datasets, calculates operational KPIs, identifies SLA performance issues, and presents actionable findings through an interactive dashboard.

The project emphasizes data quality, reproducibility, analytical reasoning, and business-focused recommendations.

---

## 19. GitHub Repository

**Repository:**

https://github.com/kavyabandaru05/Operations-sla-analytics

**Project:** Operations SLA Analytics  
**Category:** Data Analytics / Business Intelligence  
**Dataset:** Simulated Support Ticket Dataset  
**Tools:** Python, Pandas, SQL, SQLite, Power BI  
**Organization:** Arrowstack Technologies  
**Internship Domain:** Data Analytics  
**Task:** Task 2 – Operations SLA Analytics
