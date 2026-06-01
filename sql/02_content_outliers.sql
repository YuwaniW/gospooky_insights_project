CREATE OR REPLACE VIEW `gospooky-insights.gospooky_insights.content_outliers` AS
WITH platform_benchmarks AS (
  SELECT
    platform,
    ROUND(AVG(engagement_rate), 2)        AS avg_eng_rate,
    ROUND(STDDEV(engagement_rate), 2)     AS stddev_eng_rate,
    PERCENTILE_CONT(engagement_rate, 0.5)
      OVER (PARTITION BY platform)        AS median_eng_rate,
    PERCENTILE_CONT(engagement_rate, 0.9)
      OVER (PARTITION BY platform)        AS p90_eng_rate
  FROM `gospooky-insights.gospooky_insights.raw_posts`
  GROUP BY platform, engagement_rate
),
benchmarks AS (
  SELECT
    platform,
    MAX(avg_eng_rate)    AS avg_eng,
    MAX(stddev_eng_rate) AS stddev_eng,
    MAX(p90_eng_rate)    AS p90_eng
  FROM platform_benchmarks
  GROUP BY platform
)
SELECT
  p.post_id,
  p.platform,
  p.format,
  p.topic,
  p.post_date,
  p.reach,
  p.engagement_rate,
  p.creator_post,
  b.avg_eng       AS platform_avg_eng,
  b.p90_eng       AS platform_p90_eng,
  ROUND(p.engagement_rate / NULLIF(b.avg_eng, 0), 2) AS outlier_score,
  CASE
    WHEN p.engagement_rate >= b.p90_eng * 1.5 THEN 'exceptional'
    WHEN p.engagement_rate >= b.p90_eng       THEN 'strong'
    ELSE 'average'
  END AS performance_tier
FROM `gospooky-insights.gospooky_insights.raw_posts` p
JOIN benchmarks b USING (platform)
WHERE p.engagement_rate >= b.p90_eng
ORDER BY outlier_score DESC;