-- Temporary fix: Allow anon role to insert data during migration
-- Run this in Supabase SQL Editor

-- Drop the restrictive insert policy
DROP POLICY IF EXISTS "Allow authenticated users to insert" ON physicians;

-- Create a permissive policy for initial data load
CREATE POLICY "Allow anon insert for migration"
ON physicians
FOR INSERT
TO anon
WITH CHECK (true);

-- After migration is complete, you can run this to restrict it again:
-- DROP POLICY "Allow anon insert for migration" ON physicians;
-- CREATE POLICY "Allow authenticated users to insert"
-- ON physicians
-- FOR INSERT
-- TO authenticated
-- WITH CHECK (true);
