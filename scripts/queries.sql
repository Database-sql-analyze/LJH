WITH FunnelBase AS (
    SELECT 
        단계 AS step_name,
        사용자_수 AS user_count,
        LAG(사용자_수) OVER(
            ORDER BY CASE 단계
                WHEN '랜딩페이지 진입' THEN 1
                WHEN '회원가입 CTA 클릭' THEN 2
                WHEN '회원정보 입력 시작' THEN 3
                WHEN '이메일 인증 완료' THEN 4
                WHEN '가입 완료' THEN 5
                ELSE 99 
            END
        ) AS prev_user_count
    FROM 
        landing_event_log
)
SELECT 
    step_name AS "퍼널 단계",
    user_count AS "통과 사용자 수",
    
    ROUND(
        CASE 
            WHEN prev_user_count IS NULL THEN 100.0
            ELSE (user_count * 100.0) / NULLIF(prev_user_count, 0)
        END, 
        1
    ) AS "이전 단계 대비 전환율(%)",
    
    ROUND(
        CASE
            WHEN prev_user_count IS NULL THEN 0.0
            ELSE 100.0 - ((user_count * 100.0) / NULLIF(prev_user_count, 0))
        END, 
        1
    ) AS "구간 이탈률(%)"
FROM 
    FunnelBase;

WITH ChannelMetrics AS (
    SELECT 
        유입_채널 AS channel_name,
        방문자_수 AS visitor_count,
        회원가입_전환율 AS signup_rate,
        유료_전환율 AS paid_conversion_rate,
        
        CAST(REPLACE(유료_전환율, '%', '') AS FLOAT) AS paid_conversion_numeric
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
    
    ROUND(visitor_count * (paid_conversion_numeric / 100.0), 0) AS "예상 유료 고객 수",
    
    CASE 
        WHEN paid_conversion_numeric >= 2.0 THEN 'High Efficiency (Scale-up)'
        WHEN paid_conversion_numeric < 1.0 THEN 'Low Efficiency (Review Budget)'
        ELSE 'Normal'
    END AS "전략 방향성"
FROM 
    ChannelMetrics
ORDER BY 
    paid_conversion_numeric DESC;
