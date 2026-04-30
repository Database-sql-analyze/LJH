WITH FunnelBase AS (
    SELECT 
        step_name,
        user_count,
        LAG(user_count) OVER(ORDER BY step_order) as prev_user_count
    FROM 
        landing_event_log
)
SELECT 
    step_name AS "퍼널 단계",
    user_count AS "통과 사용자 수",
    ROUND((user_count * 100.0) / NULLIF(prev_user_count, 0), 1) AS "이전 단계 대비 전환율(%)",
    100.0 - ROUND((user_count * 100.0) / NULLIF(prev_user_count, 0), 1) AS "구간 이탈률(%)"
FROM 
    FunnelBase;


WITH ChannelMetrics AS (
    SELECT 
        month,
        channel_name,
        visitor_count,
        signup_rate,
        paid_conversion_rate,
        (visitor_count * (paid_conversion_rate / 100.0)) AS est_paid_users
    FROM 
        channel_performance
    WHERE 
        month = '4월'
)
SELECT 
    channel_name AS "유입 채널",
    visitor_count AS "방문자 수",
    signup_rate AS "가입 전환율(%)",
    paid_conversion_rate AS "최종 유료 전환율(%)",
    ROUND(est_paid_users, 0) AS "예상 유료 고객 수",
    CASE 
        WHEN paid_conversion_rate >= 2.0 THEN 'High Efficiency (Scale-up)'
        WHEN paid_conversion_rate < 1.0 THEN 'Low Efficiency (Review Budget)'
        ELSE 'Normal'
    END AS "전략 방향성"
FROM 
    ChannelMetrics
ORDER BY 
    paid_conversion_rate DESC;