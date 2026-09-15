# OEE Dashboard Integration

The motor protection simulator now exports `data/fault_events_oee.csv`. The file uses the same common field names accepted by the [OEE Downtime Dashboard](https://github.com/Robi46/oee-downtime-dashboard-visuals), including `availability`, `performance`, `quality`, `downtime_minutes`, `downtime_cause`, `downtime_type`, `cause`, and `reason`.

To regenerate the event log after changing a scenario, run:

```bash
python3 simulation/run_scenarios.py --csv data/fault_events_oee.csv
```

Open the OEE dashboard and upload the generated CSV through its dataset upload control. Each protection trip is represented as one minute of downtime with availability set to zero for that event row. The event-specific current, temperature, action, and source columns are retained for traceability, while the dashboard can group the records by `downtime_cause` or `cause` to build a Pareto view.

This is a file-based integration. It does not make an API request or modify the OEE dashboard repository. A future integration can append live serial events to the same schema or add a dashboard-specific ingestion endpoint.
