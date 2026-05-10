-- Experiment Readout with Guardrail Metrics
SELECT
  experiment_group,
  COUNT(DISTINCT user_id) AS users,
  AVG(conversion_rate) AS primary_conversion_rate,
  AVG(d30_retention) AS guardrail_d30_retention,
  AVG(churn_rate) AS guardrail_churn_rate,
  AVG(revenue_per_user) AS revenue_per_user
FROM nsm_product_health_data
GROUP BY experiment_group
ORDER BY primary_conversion_rate DESC;
