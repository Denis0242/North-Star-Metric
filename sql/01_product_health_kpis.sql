-- Product Health KPI Aggregation
SELECT
  DATE_TRUNC('month', event_date) AS metric_month,
  AVG(activation_rate) AS activation_rate,
  AVG(conversion_rate) AS conversion_rate,
  AVG(d30_retention) AS d30_retention,
  AVG(churn_rate) AS churn_rate,
  AVG(engagement_score) AS avg_engagement_score,
  AVG(revenue_per_user) AS revenue_per_user,
  COUNT(DISTINCT user_id) AS users
FROM nsm_product_health_data
GROUP BY 1
ORDER BY 1;
