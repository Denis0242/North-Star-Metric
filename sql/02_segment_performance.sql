-- Segment Performance
SELECT
  segment,
  COUNT(DISTINCT user_id) AS users,
  AVG(activation_rate) AS activation_rate,
  AVG(conversion_rate) AS conversion_rate,
  AVG(d30_retention) AS d30_retention,
  AVG(churn_rate) AS churn_rate,
  AVG(revenue_per_user) AS revenue_per_user,
  AVG(engagement_score) AS avg_engagement_score
FROM nsm_product_health_data
GROUP BY segment
ORDER BY conversion_rate DESC;
