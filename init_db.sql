CREATE TABLE api_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    api_name TEXT NOT NULL,
    metric_type TEXT NOT NULL, -- Par exemple: response_time, error_rate
    value REAL NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
