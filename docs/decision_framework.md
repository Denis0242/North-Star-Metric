# Decision Framework

## Primary Metric

Conversion Rate

## Guardrail Metrics

- D30 Retention
- Churn Rate
- Revenue Per User

## Decision Rules

| Scenario | Decision |
|---|---|
| Conversion improves and D30 retention is stable or better | Scale variant |
| Conversion improves but D30 retention declines | Continue monitoring |
| Conversion is flat and retention declines | Do not ship |
| Conversion declines but retention improves | Reassess product goal and segment impact |

## Current Dashboard Decision

Continue experiment monitoring before full rollout.
