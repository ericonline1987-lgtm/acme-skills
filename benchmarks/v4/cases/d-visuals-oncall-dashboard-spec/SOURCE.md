# Sources

- Google SRE Book, Chapter 6: Monitoring Distributed Systems — https://sre.google/sre-book/monitoring-distributed-systems/
- Google SRE Workbook, Alerting on SLOs — https://sre.google/workbook/alerting-on-slos/
- Grafana documentation, Dashboard best practices — https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/

## Grader basis

- symptoms-first: SRE book (symptoms vs causes; four golden signals); Grafana (alert on symptoms; RED method; general-to-specific).
- percentiles-not-averages: SRE book (averages hide the tail; use histogram buckets and high percentiles).
- error-budget-burn: SRE workbook (multiwindow, multi-burn-rate alerting; why raw error-rate thresholds are weak).
- drilldown-to-causes: SRE book (causes as debugging aids); Grafana (hierarchical drill-down, split by magnitude, directed browsing from alerts).
- lean-and-pruned: Grafana (each dashboard answers a specific question, reduce cognitive load, avoid sprawl); SRE book (dashboards answer basic questions about a service).

## Why a capable general model might miss it

Given a long list of available metrics, models tend to put every metric on the dashboard grouped by component and fall back on averages and static thresholds, instead of building from the SLO down.

The service, metrics and SLOs are synthetic.
