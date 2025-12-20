-- Database schema for healthcare events storage
-- This schema is designed to work with the advanced n8n workflow

-- Create the database (run this first if creating a new database)
-- CREATE DATABASE healthcare_analytics;

-- Connect to the database
-- \c healthcare_analytics;

-- Create the healthcare_events table
CREATE TABLE IF NOT EXISTS healthcare_events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    user_type VARCHAR(20) DEFAULT 'regular',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    event_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_event_type ON healthcare_events(event_type);
CREATE INDEX IF NOT EXISTS idx_user_id ON healthcare_events(user_id);
CREATE INDEX IF NOT EXISTS idx_user_type ON healthcare_events(user_type);
CREATE INDEX IF NOT EXISTS idx_timestamp ON healthcare_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_event_data_gin ON healthcare_events USING GIN(event_data);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update the updated_at column
CREATE TRIGGER update_healthcare_events_updated_at 
    BEFORE UPDATE ON healthcare_events 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Create a view for daily event summaries
CREATE OR REPLACE VIEW daily_event_summary AS
SELECT 
    DATE(timestamp) as event_date,
    event_type,
    user_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users
FROM healthcare_events
GROUP BY DATE(timestamp), event_type, user_type
ORDER BY event_date DESC, event_count DESC;

-- Create a view for user engagement metrics
CREATE OR REPLACE VIEW user_engagement_metrics AS
SELECT 
    user_id,
    user_type,
    COUNT(*) as total_events,
    COUNT(DISTINCT event_type) as event_diversity,
    MIN(timestamp) as first_activity,
    MAX(timestamp) as last_activity,
    EXTRACT(EPOCH FROM (MAX(timestamp) - MIN(timestamp))) / 3600 as engagement_duration_hours
FROM healthcare_events
GROUP BY user_id, user_type
ORDER BY total_events DESC;

-- Create a materialized view for performance analytics (refresh periodically)
CREATE MATERIALIZED VIEW IF NOT EXISTS event_performance_analytics AS
SELECT 
    event_type,
    user_type,
    COUNT(*) as total_events,
    COUNT(DISTINCT user_id) as unique_users,
    AVG(EXTRACT(EPOCH FROM (timestamp - LAG(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp)))) as avg_time_between_events_seconds,
    MIN(timestamp) as first_recorded,
    MAX(timestamp) as last_recorded
FROM healthcare_events
GROUP BY event_type, user_type;

-- Create indexes for the materialized view
CREATE INDEX IF NOT EXISTS idx_event_perf_type ON event_performance_analytics(event_type);
CREATE INDEX IF NOT EXISTS idx_event_perf_user_type ON event_performance_analytics(user_type);

-- Sample queries for monitoring and analysis:

-- 1. Get recent events for a specific user
-- SELECT * FROM healthcare_events WHERE user_id = 'user_xxxxxxxx' ORDER BY timestamp DESC LIMIT 10;

-- 2. Get daily event counts
-- SELECT DATE(timestamp) as date, COUNT(*) as events FROM healthcare_events GROUP BY DATE(timestamp) ORDER BY date DESC;

-- 3. Get user type distribution
-- SELECT user_type, COUNT(*) as count FROM healthcare_events GROUP BY user_type ORDER BY count DESC;

-- 4. Get most active users
-- SELECT user_id, COUNT(*) as event_count FROM healthcare_events GROUP BY user_id ORDER BY event_count DESC LIMIT 10;

-- 5. Get event type distribution
-- SELECT event_type, COUNT(*) as count FROM healthcare_events GROUP BY event_type ORDER BY count DESC;

-- 6. Refresh the materialized view (run periodically)
-- REFRESH MATERIALIZED VIEW event_performance_analytics;

-- Grant appropriate permissions (adjust as needed for your security requirements)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON healthcare_events TO your_application_user;
-- GRANT SELECT ON ALL VIEWS IN SCHEMA public TO your_analytics_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_application_user;