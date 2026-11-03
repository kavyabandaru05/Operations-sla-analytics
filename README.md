# Operations SLA Analytics Dashboard

An end-to-end Data Analytics project that analyzes support ticket operations, SLA compliance, resolution efficiency, root causes, and customer satisfaction using Python, Pandas, SQL, SQLite, and Power BI.

---

## 1. Project Overview

The Operations SLA Analytics project focuses on analyzing support ticket data to evaluate operational performance and identify opportunities for improving service quality.

The project processes a simulated support ticket dataset containing 6,661 raw records. It performs data cleaning, data validation, SQL-based KPI analysis, automated business insights generation, and interactive Power BI dashboard development.

The final solution provides insights into SLA breaches, team performance, ticket resolution trends, root causes, and customer satisfaction.

## 2. Business Objectives

- Monitor SLA compliance and breach rates.
- Identify teams experiencing operational delays.
- Analyze ticket volume and resolution trends.
- Identify major root causes of SLA breaches.
- Understand customer satisfaction patterns.
- Provide actionable recommendations for operations managers.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Data processing and automation |
| Pandas | Data cleaning and transformation |
| SQL | KPI analysis and business queries |
| SQLite | Structured data storage |
| Power BI | Interactive dashboard and visualization |
| VS Code | Development environment |
| Git and GitHub | Version control |

## 4. Project Architecture

```text
Raw Support Ticket Dataset
          |
          v
Python Data Cleaning & Validation
          |
          v
Cleaned Ticket Dataset
          |
          v
SQLite Database
          |
          v
SQL KPI Analysis
          |
          v
KPI Analysis Results
          |
          +----------------------+
          |                      |
          v                      v
Power BI Dashboard       Automated Insights
          |                      |
          v                      v
Interactive Analysis    Executive Summary
```

## 5. Project Structure

```text
project-2-sla-analytics/
│
├── data/
│   ├── tickets_raw.csv
│   ├── tickets_clean.csv
│   └── sla_analytics.db
│
├── dashboard/
│   ├── Operations_SLA_Analytics.pbix
│   ├── kpi_team.csv
│   └── kpi_weekday.csv
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
└── README.md
```

## 6. Data Processing and Cleaning

The raw dataset contains 6,661 records.

The data cleaning process includes:

- Standardizing priority values.
- Removing exact duplicate records.
- Handling missing and invalid priority values.
- Handling missing team information.
- Validating ticket timestamps.
- Removing invalid response and resolution timestamps.
- Validating SLA targets against ticket priority.
- Handling invalid CSAT scores.
- Identifying extreme resolution durations.
- Calculating resolution and response durations.
- Identifying SLA breaches.

### Data Cleaning Summary

| Metric | Result |
|---|---:|
| Raw records | 6,661 |
| Cleaned records | 6,656 |
| Exact duplicate records removed | 1 |
| Final cleaned records | 6,656 |

## 7. Key Performance Indicators

The following KPIs were calculated using SQL and displayed in the Power BI dashboard.

| KPI | Result |
|---|---:|
| Total Tickets | 6,656 |
| SLA Breach Rate | 36.09% |
| Average Resolution Time | 29.16 hours |
| Average First Response Time | 3.78 hours |
| Reopened Ticket Rate | 5.86% |
| Average CSAT | 3.77 / 5 |
| Backlog | 146 |

### SLA Calculation

SLA breaches are identified by comparing ticket resolution duration with the SLA target assigned to the ticket priority.

For unresolved tickets, ticket age is calculated using the project's fixed analysis snapshot.

SLA calculations use calendar hours rather than business hours.

## 8. Power BI Dashboard

The interactive Power BI dashboard provides a consolidated view of support ticket performance.

### KPI Cards

- Total Tickets
- SLA Breach Percentage
- Average Resolution Hours
- Average First Response Hours
- Backlog
- Average Customer Satisfaction
- Reopened Ticket Percentage

### Analytical Visualizations

1. Monthly Ticket Volume and SLA Breach Trend.
2. Ticket Volume by Weekday and Channel.
3. Average Resolution Time vs SLA Target by Priority.
4. SLA Breach Rate by Team.
5. SLA Breaches by Root Cause.
6. Customer Satisfaction: SLA Breached vs Not Breached.

### Interactive Filters

The dashboard includes page-level filters for:

- Month
- Team
- Priority
- Channel
- Customer Tier

These filters allow users to explore operational performance across different dimensions.

## 9. Key Business Insights

1. **Team Performance:** Logistics recorded the highest SLA breach rate at 55.14%, followed by Billing at 48.05%.

2. **Monthly Trend:** December 2025 recorded the highest monthly SLA breach rate at 41.45%.

3. **Root Cause Analysis:** Performance issues contributed the highest number of SLA breaches, with 228 breached tickets.

4. **Customer Satisfaction:** Tickets without SLA breaches had an average CSAT of 4.07, compared with 3.24 for tickets with SLA breaches.

5. **SLA Compliance:** Overall, 36.09% of tickets breached their SLA targets.

## 10. Business Recommendations

Based on the analysis, the following recommendations can help improve support operations:

- Review workload distribution and resolution workflows in the Logistics and Billing teams.
- Investigate recurring performance issues and prioritize preventive maintenance.
- Introduce early-warning alerts for tickets approaching SLA deadlines.
- Monitor high-volume months and plan staffing capacity accordingly.
- Improve customer communication when ticket resolution is delayed.
- Track SLA compliance and customer satisfaction together.

## 11. Data Quality Testing

A Python-based automated data-quality testing framework was implemented.

The framework validates:

- Dataset availability.
- Unique ticket identifiers.
- Duplicate records.
- Required columns.
- Valid SLA breach flags.
- Valid reopened flags.
- Positive SLA targets.
- CSAT values within the 1–5 range.
- Valid first-response timestamps.
- CSV and SQLite row-count consistency.

### Test Results

| Metric | Result |
|---|---:|
| Total Tests | 10 |
| Passed | 10 |
| Failed | 0 |

**All 10 automated data-quality tests passed successfully.**

Test evidence is available in:

`reports/data_quality_test_results.csv`

## 12. How to Run the Project

### Prerequisites

- Python 3.13 or a compatible Python version.
- Pandas.
- SQLite support.
- Power BI Desktop.

### Install Dependencies

Run the following command in the terminal:

```powershell
py -m pip install pandas
```

### Execute the Data Analytics Pipeline

Run the following commands from the project root directory.

**Step 1: Generate the simulated dataset (optional)**

```powershell
py generate_data.py
```

Run this only when you want to regenerate the original simulated dataset.

**Step 2: Clean and validate the data**

```powershell
py clean_and_validate.py
```

**Step 3: Load cleaned data into SQLite**

```powershell
py load_to_sqlite.py
```

**Step 4: Execute SQL KPI queries**

```powershell
py run_kpi_queries.py
```

**Step 5: Generate automated business insights**

```powershell
py generate_insights.py
```

**Step 6: Run automated data-quality tests**

```powershell
py test_data_quality.py
```

### Open the Power BI Dashboard

Open the following file using Power BI Desktop:

`dashboard/Operations_SLA_Analytics.pbix`

## 13. Project Documentation

Additional project documentation is available in the `docs/` and `reports/` folders.

| Document | Description |
|---|---|
| requirements.md | Business requirements and project scope |
| implementation.md | Technical implementation details |
| decision_log.md | Important technical decisions |
| work_log.md | Project development activities |
| validation_log.csv | Data cleaning and validation evidence |
| powerbi_build_guide.md | Power BI dashboard implementation |
| executive_summary.md | Key findings and business recommendations |
| automated_insights_report.txt | Automatically generated analytical insights |
| data_quality_test_results.csv | Automated test results |

## 14. Limitations

- The dataset is simulated and does not represent actual company operations.
- SLA calculations use calendar hours rather than business hours.
- Business-hours and holiday calendars are not implemented.
- Real-time monitoring and ticketing-system integration are outside the current project scope.
- The relationship between SLA breaches and customer satisfaction is observational and does not establish causation.

## 15. Future Enhancements

- Real-time SLA monitoring.
- Automated SLA breach notifications.
- Predictive ticket-volume analysis.
- Business-hours SLA calculations.
- Agent workload and performance analysis.
- Integration with production ticket management systems.
- Machine learning-based ticket priority prediction.

## 16. Conclusion

The Operations SLA Analytics project demonstrates an end-to-end data analytics workflow, from raw data cleaning and validation to SQL-based KPI analysis and interactive Power BI reporting.

The solution identifies operational bottlenecks, highlights SLA breach patterns, and provides actionable recommendations to improve support operations and customer satisfaction.

The project also demonstrates practical skills in Python, Pandas, SQL, SQLite, Power BI, data validation, and business intelligence.

---

**Project:** Operations SLA Analytics  
**Category:** Data Analytics / Business Intelligence  
**Dataset:** Simulated Support Ticket Dataset  
**Tools:** Python, Pandas, SQL, SQLite, Power BI