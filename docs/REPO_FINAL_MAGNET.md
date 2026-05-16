# North Star Metric & Product Health Dashboard

![Dashboard Preview](screenshots/dashboard_preview.png)

## Executive Summary
This project analyzes **North Star Metric (NSM) and product health performance** across digital product users to help product, growth, and executive teams understand activation, conversion, retention, churn risk, feature adoption, engagement, and monetization.

The dashboard evaluates **activation rate, conversion rate, D30 retention, churn rate, average engagement score, revenue per user, channel performance, segment performance, feature adoption, and experiment readout** to identify where product experience is healthy and where intervention is needed.

**Decision Supported:** Which segments, channels, features, and experiment groups should receive deeper investment, monitoring, or optimization.

**Business Outcome:** Improve product health, increase retention, reduce churn risk, improve engagement, and support better product roadmap decisions.

**Tech Stack:** Tableau • SQL • Python • Streamlit • Product Analytics

---

## Business Problem
Product and growth teams need more than isolated KPI reporting. Leadership needs a single readout that answers:

> Is the product growing in a healthy way, and which segments, channels, or features need action?

This repo turns product usage data into an executive-ready product health dashboard using KPI monitoring, retention analysis, segmentation, feature adoption, channel comparison, and experiment group readout.

---

## KPI Goals

| KPI | Business Purpose |
|---|---|
| Activation Rate | Measures early user value realization |
| Conversion Rate | Measures successful product action completion |
| D30 Retention | Measures durable product stickiness |
| Churn Rate | Measures user loss risk |
| Avg Engagement Score | Measures overall product interaction quality |
| Revenue Per User | Measures monetization strength |
| Feature Adoption Rate | Measures usage of core product capabilities |
| Channel Performance | Identifies acquisition sources driving stronger users |
| Segment Performance | Shows which customer segments perform best |
| Experiment Group | Supports product testing and rollout decisions |

---

## Dataset Overview

| Item | Value |
|---|---:|
| Dataset | `data/processed/nsm_dataset_clean.csv` |
| Rows | 920 |
| Columns | 23 |
| Date Range | 2025-01-01 to 2026-01-01 |
| Countries | 5 |
| Segments | 3 |
| Devices | 3 |
| Experiment Groups | 3 |
| Primary Features | 5 |

Key fields include:

```text
user_id, event_date, country, segment, device, acquisition_channel,
primary_feature_used, experiment_group, DAU, WAU, MAU, stickiness_ratio,
conversion_rate, d1_retention, d7_retention, d30_retention, churn_rate,
revenue_per_user, session_frequency, activation_rate, feature_adoption_rate,
engagement_score, engagement_band
```

---

## Metrics Engineering

| Metric | Formula / Logic |
|---|---|
| Activation Rate | Activated Users / Total Users |
| Conversion Rate | Converted Users / Total Users |
| D30 Retention | Users active after 30 days / Total Users |
| Churn Rate | 1 − Retention Rate |
| Revenue Per User | Total Revenue / Users |
| Stickiness Ratio | DAU / MAU |
| Feature Adoption Rate | Users adopting a feature / Eligible users |
| Engagement Band | Low / Medium / High classification based on engagement score |

---

## Representative SQL Queries

### 1. Executive KPI Summary
```sql
SELECT
    AVG(activation_rate) AS avg_activation_rate,
    AVG(conversion_rate) AS avg_conversion_rate,
    AVG(d30_retention) AS avg_d30_retention,
    AVG(churn_rate) AS avg_churn_rate,
    AVG(engagement_score) AS avg_engagement_score,
    AVG(revenue_per_user) AS avg_revenue_per_user
FROM nsm_product_health;
```

### 2. Product Health Trend Over Time
```sql
SELECT
    DATE_TRUNC('month', event_date) AS month,
    AVG(activation_rate) AS activation_rate,
    AVG(conversion_rate) AS conversion_rate,
    AVG(d30_retention) AS d30_retention,
    AVG(churn_rate) AS churn_rate
FROM nsm_product_health
GROUP BY 1
ORDER BY 1;
```

### 3. Performance by Segment
```sql
SELECT
    segment,
    AVG(conversion_rate) AS conversion_rate,
    AVG(d30_retention) AS d30_retention,
    AVG(revenue_per_user) AS revenue_per_user,
    AVG(engagement_score) AS engagement_score
FROM nsm_product_health
GROUP BY 1
ORDER BY engagement_score DESC;
```

### 4. Feature Adoption by Feature
```sql
SELECT
    primary_feature_used,
    AVG(feature_adoption_rate) AS feature_adoption_rate,
    AVG(conversion_rate) AS conversion_rate,
    AVG(d30_retention) AS d30_retention
FROM nsm_product_health
GROUP BY 1
ORDER BY feature_adoption_rate DESC;
```

---

## Dashboard Preview

### Main Executive Dashboard
![Main Dashboard](screenshots/dashboard_preview.png)

### KPI Overview
![KPI Overview](screenshots/kpi_overview.png)

### Trend and Segment View
![Trend and Segment View](screenshots/trend_and_segment_view.png)

### Retention, Experiment, and Channel View
![Retention Experiment Channel View](screenshots/retention_experiment_channel_view.png)

---

## Product Insights

### Insight
Variant B leads conversion performance but trails D30 retention, meaning the variant shows growth potential but needs retention monitoring before full rollout.

### Action
Prioritize deeper testing of Variant B while monitoring D30 retention, churn risk, and revenue per user across segments and channels.

### Recommendation
Scale Variant B only if D30 retention remains stable and churn risk does not increase after rollout.

### Decision
**Continue experiment monitoring before full rollout.**

---

## Measurable Business Impact
This product health dashboard can help teams:

- Improve activation and conversion by identifying stronger segments, channels, and feature experiences.
- Reduce churn risk by monitoring retention and churn movement before scaling product changes.
- Improve product roadmap prioritization by showing which features drive stronger adoption.
- Increase monetization focus by comparing revenue per user across segments and channels.
- Shorten executive decision cycles by turning product health data into a single KPI readout.

Example scenario:

```text
If Variant B improves conversion by 5–8% but weakens D30 retention, leadership can avoid a risky full rollout and continue targeted testing before scaling.
```

---

## Streamlit App
Run locally:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

The Streamlit app recreates the Tableau dashboard story with KPI cards, filters, charts, and an executive decision summary.

---

## Repo Architecture

```text
North-Star-Metric-Product-Health-Repo/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   │   └── nsm_dataset_raw.csv
│   └── processed/
│       └── nsm_dataset_clean.csv
├── dashboard/
│   └── nsm_tableau_dashboard_reference.png
├── docs/
│   ├── business_case.md
│   ├── dashboard_guide.md
│   └── kpi_definitions.md
├── notebooks/
│   └── eda_cleaning_feature_engineering.ipynb
├── screenshots/
│   ├── dashboard_preview.png
│   ├── kpi_overview.png
│   ├── trend_and_segment_view.png
│   └── retention_experiment_channel_view.png
├── sql/
│   ├── representative_queries.sql
│   └── kpi_views.sql
├── tests/
│   └── test_data_quality.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Healthcare & Product Analytics Relevance
This framework can support healthcare and digital health products by evaluating:

- patient onboarding activation
- appointment booking conversion
- digital care feature adoption
- care-program retention
- churn risk in patient engagement journeys

---

## Future Improvements
- Add cohort retention heatmaps.
- Add statistical testing for experiment groups.
- Add predictive churn-risk scoring.
- Connect to Snowflake or Redshift.
- Add Prefect pipeline for scheduled refresh.
