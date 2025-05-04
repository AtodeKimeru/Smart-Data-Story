WITH issue_events AS (
    SELECT
        repo_name,
        DATE(created_at) AS event_date,
        COUNT(*) AS closed_issues_count
    FROM {{ ref('github_events_cleaned') }}
    WHERE type = 'IssuesEvent'
    AND payload->>'action' = 'closed'
    GROUP BY repo_name, DATE(created_at)
),

push_events AS (
    SELECT
        repo_name,
        DATE(created_at) AS event_date,
        COUNT(*) AS push_count
    FROM {{ ref('github_events_cleaned') }}
    WHERE type = 'PushEvent'
    GROUP BY repo_name, DATE(created_at)
)

SELECT
    COALESCE(i.repo_name, p.repo_name) AS repo_name,
    COALESCE(i.event_date, p.event_date) AS event_date,
    COALESCE(i.closed_issues_count, 0) AS closed_issues_count,
    COALESCE(p.push_count, 0) AS push_count,
    CASE 
        WHEN COALESCE(p.push_count, 0) = 0 THEN NULL
        ELSE ROUND(CAST(COALESCE(i.closed_issues_count, 0) AS FLOAT) / NULLIF(p.push_count, 0), 3)
    END AS issues_to_push_ratio
FROM issue_events i
FULL OUTER JOIN push_events p
    ON i.repo_name = p.repo_name
    AND i.event_date = p.event_date
WHERE COALESCE(i.closed_issues_count, 0) > 0 OR COALESCE(p.push_count, 0) > 0
ORDER BY event_date DESC, repo_name
