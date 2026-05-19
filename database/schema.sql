CREATE TABLE IF NOT EXISTS electricity_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meter_id TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    voltage REAL,
    consumption REAL
);