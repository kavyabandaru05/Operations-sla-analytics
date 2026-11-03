
-- ============================================================
-- PROJECT 2: OPERATIONS SLA ANALYTICS
-- KPI QUERIES
-- Database: SQLite
-- Source: data/tickets_clean.csv
-- Table: tickets
-- Reporting Snapshot: 31 December 2025
-- ============================================================

-- SLA BREACH DEFINITION:
-- Resolved tickets:
--     resolution_hours > sla_target_hours
--
-- Open / In Progress tickets:
--     Ticket age at reporting snapshot > sla_target_hours
--
-- Resolution-time metrics:
--     Calculated only for tickets with a valid resolution time.
--
-- Missing CSAT:
--     Excluded automatically by AVG(csat_score).


-- ============================================================
-- Q1: HEADLINE BUSINESS KPIs
-- ============================================================

SELECT
    COUNT(*) AS total_tickets,

    ROUND(
        100.0 * SUM(sla_breached) / COUNT(*), 2
    ) AS sla_breach_pct,

    ROUND(
        AVG(resolution_hours), 2
    ) AS avg_resolution_hrs,

    ROUND(
        AVG(first_response_hours), 2
    ) AS avg_first_response_hrs,

    ROUND(
        100.0 * SUM(reopened) / COUNT(*), 2
    ) AS reopen_pct,

    ROUND(
        AVG(csat_score), 2
    ) AS avg_csat,

    SUM(
        CASE
            WHEN status IN ('Open', 'In Progress')
            THEN 1
            ELSE 0
        END
    ) AS backlog

FROM tickets;


-- ============================================================
-- Q2: MONTHLY TICKET VOLUME AND SLA BREACH TREND
-- ============================================================

SELECT
    created_month,

    COUNT(*) AS total_tickets,

    SUM(sla_breached) AS breached_tickets,

    ROUND(
        100.0 * SUM(sla_breached) / COUNT(*), 2
    ) AS breach_pct,

    ROUND(
        AVG(resolution_hours), 2
    ) AS avg_resolution_hrs

FROM tickets

GROUP BY created_month

ORDER BY created_month;


-- ============================================================
-- Q3: PRIORITY-WISE SLA PERFORMANCE
-- ============================================================

SELECT
    priority,

    sla_target_hours,

    COUNT(*) AS total_tickets,

    SUM(sla_breached) AS breached_tickets,

    ROUND(
        100.0 * SUM(sla_breached) / COUNT(*), 2
    ) AS breach_pct,

    ROUND(
        AVG(resolution_hours), 2
    ) AS avg_resolution_hrs

FROM tickets

GROUP BY
    priority,
    sla_target_hours

ORDER BY sla_target_hours;


-- ============================================================
-- Q4: TEAM-WISE OPERATIONAL PERFORMANCE
-- ============================================================

SELECT
    team,

    COUNT(*) AS total_tickets,

    SUM(sla_breached) AS breached_tickets,

    ROUND(
        100.0 * SUM(sla_breached) / COUNT(*), 2
    ) AS breach_pct,

    ROUND(
        AVG(resolution_hours), 2
    ) AS avg_resolution_hrs,

    ROUND(
        AVG(first_response_hours), 2
    ) AS avg_first_response_hrs,

    ROUND(
        AVG(csat_score), 2
    ) AS avg_csat

FROM tickets

GROUP BY team

ORDER BY breach_pct DESC;


-- ============================================================
-- Q5: ROOT-CAUSE ANALYSIS AND BREACH CONTRIBUTION
-- ============================================================

SELECT
    root_cause,

    team,

    COUNT(*) AS total_tickets,

    SUM(sla_breached) AS breached_tickets,

    ROUND(
        100.0 * SUM(sla_breached) / COUNT(*), 2
    ) AS breach_pct,

    ROUND(
        100.0 * SUM(sla_breached) /
        NULLIF(
            (SELECT SUM(sla_breached) FROM tickets), 0
        ), 2
    ) AS share_of_all_breaches

FROM tickets

GROUP BY
    root_cause,
    team

ORDER BY
    breached_tickets DESC,
    breach_pct DESC;


-- ============================================================
-- Q6: WEEKDAY AND CHANNEL ANALYSIS
-- ============================================================

SELECT
    weekday,

    channel,

    COUNT(*) AS total_tickets,

    SUM(sla_breached) AS breached_tickets,

    ROUND(
        100.0 * SUM(sla_breached) / COUNT(*), 2
    ) AS breach_pct,

    ROUND(
        AVG(first_response_hours), 2
    ) AS avg_first_response_hrs

FROM tickets

GROUP BY
    weekday,
    channel

ORDER BY total_tickets DESC;


-- ============================================================
-- Q7: RELATIONSHIP BETWEEN SLA BREACH AND CUSTOMER SATISFACTION
-- ============================================================

SELECT
    sla_breached,

    COUNT(*) AS total_tickets,

    COUNT(csat_score) AS rated_tickets,

    ROUND(
        AVG(csat_score), 2
    ) AS avg_csat,

    ROUND(
        100.0 * COUNT(csat_score) / COUNT(*), 2
    ) AS csat_response_pct

FROM tickets

GROUP BY sla_breached

ORDER BY sla_breached;


-- ============================================================
-- END OF KPI QUERIES
-- ============================================================
