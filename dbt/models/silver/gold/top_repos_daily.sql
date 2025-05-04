SELECT
    repo_name,
    DATE(created_at) AS event_date,
    COUNT(*) AS event_count
FROM {{ ref('github_events_cleaned') }}
GROUP BY repo_name, event_date
ORDER BY event_date DESC, event_count DESC