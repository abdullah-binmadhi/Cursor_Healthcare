-- Healthcare Website Database Schema for Supabase
-- Run this in your Supabase SQL Editor

-- Create physicians table
CREATE TABLE IF NOT EXISTS physicians (
    id TEXT PRIMARY KEY,
    physician_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    department_id TEXT,
    hospital TEXT NOT NULL,
    rating DECIMAL(3,1) DEFAULT 4.5,
    availability TEXT DEFAULT 'available',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_physicians_specialty ON physicians(specialty);
CREATE INDEX IF NOT EXISTS idx_physicians_hospital ON physicians(hospital);
CREATE INDEX IF NOT EXISTS idx_physicians_rating ON physicians(rating);
CREATE INDEX IF NOT EXISTS idx_physicians_availability ON physicians(availability);

-- Enable Row Level Security (RLS)
ALTER TABLE physicians ENABLE ROW LEVEL SECURITY;

-- Create policy to allow public read access (for website visitors)
CREATE POLICY "Allow public read access"
ON physicians
FOR SELECT
TO anon
USING (true);

-- Create policy to allow authenticated users to insert/update (for admin panel)
CREATE POLICY "Allow authenticated users to insert"
ON physicians
FOR INSERT
TO authenticated
WITH CHECK (true);

CREATE POLICY "Allow authenticated users to update"
ON physicians
FOR UPDATE
TO authenticated
USING (true)
WITH CHECK (true);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_physicians_updated_at 
    BEFORE UPDATE ON physicians
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create a view for quick stats
CREATE OR REPLACE VIEW physician_stats AS
SELECT 
    COUNT(*) as total_physicians,
    COUNT(DISTINCT specialty) as total_specialties,
    COUNT(DISTINCT hospital) as total_hospitals,
    AVG(rating) as average_rating,
    COUNT(*) FILTER (WHERE availability = 'available') as available_physicians
FROM physicians;

-- Grant access to the view
GRANT SELECT ON physician_stats TO anon;
GRANT SELECT ON physician_stats TO authenticated;
