CREATE OR REPLACE TABLE `gospooky-insights.gospooky_insights.weekly_summary` AS

WITH weekly_agg AS (
  SELECT
    DATE_TRUNC(post_date, WEEK(MONDAY))   AS week_start,
    platform,
    format,
    COUNT(*)                              AS total_posts,
    SUM(reach)                            AS total_reach,
    SUM(impressions)                      AS total_impressions,
    ROUND(AVG(engagement_rate), 2)        AS avg_eng_rate,
    SUM(likes)                            AS total_likes,
    SUM(comments)                         AS total_comments,
    SUM(shares)                           AS total_shares,
    SUM(saves)                            AS total_saves,
    SUM(video_views)                      AS total_video_views,
    COUNTIF(creator_post = TRUE)          AS creator_posts,
    COUNTIF(creator_post = FALSE)         AS brand_posts
  FROM `gospooky-insights.gospooky_insights.raw_posts`
  GROUP BY 1, 2, 3
)

SELECT
  *,
  ROUND(
    (total_reach - LAG(total_reach) OVER (
      PARTITION BY platform, format
      ORDER BY week_start
    )) / NULLIF(LAG(total_reach) OVER (
      PARTITION BY platform, format
      ORDER BY week_start
    ), 0) * 100
  , 1) AS reach_wow_pct
FROM weekly_agg
ORDER BY week_start DESC;