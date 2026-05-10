-- Feature Adoption and Engagement
SELECT
  primary_feature_used,
  COUNT(DISTINCT user_id) AS users,
  AVG(feature_adoption_rate) AS feature_adoption_rate,
  AVG(conversion_rate) AS conversion_rate,
  AVG(engagement_score) AS avg_engagement_score
FROM nsm_product_health_data
GROUP BY primary_feature_used
ORDER BY feature_adoption_rate DESC;
