# Decision Log

| # | Decision | Reason | Trade-off |
|---|---|---|---|
| 1 | Calendar hours for SLA | No business-hours calendar supplied | Overstates breaches for tickets raised at night or on weekends |
| 2 | Open tickets past target count as breached | A ticket already over target has failed its SLA even if unresolved | Some may be closed later; snapshot date 31-Dec-2025 fixed |
| 3 | Resolution-time averages use resolved tickets only | Open tickets have no end time | Slightly optimistic average |
| 4 | Missing priority row removed | SLA target cannot be assigned reliably | 1 row lost |
| 5 | Missing team set to "Unassigned" | Ticket is otherwise valid | Adds a one-row team to charts; exclude with a filter |
| 6 | Resolution > 2,000 h treated as outlier and removed | Looks like a data-entry error (about 250 days) | A genuine long case would be lost; flagged in log |
| 7 | CSAT outside 1-5 set to blank, not removed | Rest of the ticket is valid | None |
| 8 | Breach % uses all tickets as denominator | Keeps open breaches in scope | Differs from "resolved only" definitions |
