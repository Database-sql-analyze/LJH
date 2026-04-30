WITH FunnelBase AS (
    SELECT 
        단계 AS step_name,
        사용자_수 AS user_count,
        -- LAG 함수를 사용하여 이전 단계의 사용자 수를 가져옴 (첫 단계는 NULL 반환)
        LAG(사용자_수) OVER() AS prev_user_count
    FROM 
        landing_event_log
)
SELECT 
    step_name AS "퍼널 단계",
    user_count AS "통과 사용자 수",
    
    -- [핵심 수정] COALESCE를 사용하여 첫 단계(prev_user_count가 NULL)일 경우 
    -- 자기 자신의 사용자 수를 분모로 사용하여 에러 및 NULL 결과값을 방지함
    ROUND(
        (user_count * 100.0) / NULLIF(COALESCE(prev_user_count, user_count), 0), 
        1
    ) AS "이전 단계 대비 전환율(%)",
    
    100.0 - ROUND(
        (user_count * 100.0) / NULLIF(COALESCE(prev_user_count, user_count), 0), 
        1
    ) AS "구간 이탈률(%)"
FROM 
    FunnelBase;


-- =======================================================================
-- [Query 2] 유입 채널별 투자 대비 효율(ROI) 및 타당성 검증
-- =======================================================================
WITH ChannelMetrics AS (
    SELECT 
        유입_채널 AS channel_name,
        방문자_수 AS visitor_count,
        회원가입_전환율 AS signup_rate,
        유료_전환율 AS paid_conversion_rate,
        
        -- 최종 결제 유저 수 추정치 계산 (방문자 수 * 유료 전환율)
        (방문자_수 * (CAST(REPLACE(유료_전환율, '%', '') AS FLOAT) / 100.0)) AS est_paid_users
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
    
    -- 비즈니스 인사이트 플래그 생성: 데이터 기반 전략적 의사결정 제안
    CASE 
        WHEN CAST(REPLACE(paid_conversion_rate, '%', '') AS FLOAT) >= 2.0 THEN 'High Efficiency (Scale-up)'
        WHEN CAST(REPLACE(paid_conversion_rate, '%', '') AS FLOAT) < 1.0 THEN 'Low Efficiency (Review Budget)'
        ELSE 'Normal'
    END AS "전략 방향성"
FROM 
    ChannelMetrics
ORDER BY 
    CAST(REPLACE(paid_conversion_rate, '%', '') AS FLOAT) DESC;
