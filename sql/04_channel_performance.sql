-- Acquisition Channel Quality
SELECT
  acquisition_channel,
  COUNT(DISTINCT user_id) AS users,
  AVG(conversion_rate) AS conversion_rate,
  AVG(d30_retention) AS d30_retention,
  AVG(revenue_per_user) AS revenue_per_user,
  AVG(churn_rate) AS churn_rate
FROM nsm_product_health_data
GROUP BY acquisition_channel
ORDER BY conversion_rate DESC;
