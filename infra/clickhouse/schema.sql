CREATE DATABASE IF NOT EXISTS logs;

CREATE TABLE IF NOT EXISTS logs.raw_logs
(
    timestamp   DateTime,
    tenant_id   String,
    service     String,
    level       LowCardinality(String),
    message     String,
    trace_id    String
)
ENGINE = MergeTree
PARTITION BY toDate(timestamp)
ORDER BY (tenant_id, service, timestamp)
TTL
    timestamp + INTERVAL 7 DAY DELETE WHERE level = 'INFO',
    timestamp + INTERVAL 14 DAY DELETE WHERE level = 'WARN',
    timestamp + INTERVAL 30 DAY DELETE WHERE level = 'ERROR'
SETTINGS index_granularity = 8192;