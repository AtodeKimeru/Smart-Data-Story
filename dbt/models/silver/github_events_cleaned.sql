WITH raw AS (
    SELECT *
    FROM {{ source('github', 'github_raw_events') }}
)

SELECT
    id,
    type,
    actor->>'login' AS actor_login,
    repo->>'name' AS repo_name,
    payload,
    public,
    created_at
FROM raw
WHERE created_at IS NOT NULL
