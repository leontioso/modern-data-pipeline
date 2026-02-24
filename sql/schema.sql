-- Data Warehouse Schema
-- Core tables for the data pipeline

-- Raw data landing zone
CREATE TABLE IF NOT EXISTS raw.events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    event_data JSONB,
    source_system VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Staging tables
CREATE TABLE IF NOT EXISTS staging.products (
    id INTEGER,
    name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10, 2),
    source_system VARCHAR(100),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics tables
CREATE TABLE IF NOT EXISTS analytics.product_summary (
    category VARCHAR(100),
    total_products INTEGER,
    avg_price DECIMAL(10, 2),
    min_price DECIMAL(10, 2),
    max_price DECIMAL(10, 2),
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_events_source ON raw.events(source_system);
CREATE INDEX IF NOT EXISTS idx_events_type ON raw.events(event_type);
CREATE INDEX IF NOT EXISTS idx_products_category ON staging.products(category);
