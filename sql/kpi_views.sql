-- Representative SQL Queries for North Star Metric & Product Health Dashboard

-- 1. Executive KPI Summary
SELECT
    AVG(activation_rate) AS avg_activation_rate,
    AVG(conversion_rate) AS avg_conversion_rate,
    AVG(d30_retention) AS avg_d30_retention,
    AVG(churn_rate) AS avg_churn_rate,
    AVG(engagement_score) AS avg_engagement_score,
    AVG(revenue_per_user) AS avg_revenue_per_user
FROM nsm_product_health;

-- 2. Product Health Trend Over Time
SELECT
    DATE_TRUNC('month', event_date) AS month,
    AVG(activation_rate) AS activation_rate,
    AVG(conversion_rate) AS conversion_rate,
    AVG(d30_retention) AS d30_retention,
    AVG(churn_rate) AS churn_rate
FROM nsm_product_health
GROUP BY 1
ORDER BY 1;

-- 3. Performance by Segment
SELECT
    segment,
    AVG(conversion_rate) AS conversion_rate,
    AVG(d30_retention) AS d30_retention,
    AVG(revenue_per_user) AS revenue_per_user,
    AVG(engagement_score) AS engagement_score
FROM nsm_product_health
GROUP BY 1
ORDER BY engagement_score DESC;

-- 4. Feature Adoption by Feature
SELECT
    primary_feature_used,
    AVG(feature_adoption_rate) AS feature_adoption_rate,
    AVG(conversion_rate) AS conversion_rate,
    AVG(d30_retention) AS d30_retention
FROM nsm_product_health
GROUP BY 1
ORDER BY feature_adoption_rate DESC;
