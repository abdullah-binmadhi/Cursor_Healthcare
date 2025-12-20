/**
 * Supabase Client Configuration
 * Healthcare Website v2
 */
import { createClient } from '@supabase/supabase-js';

// Supabase project configuration
// Note: The anon key is safe for client-side use (it only allows public read access)
const SUPABASE_URL = 'https://pdgumgpjoeojbojacung.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkZ3VtZ3Bqb2VvamJvamFjdW5nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1NjQ5NTYsImV4cCI6MjA4MTE0MDk1Nn0.aRtltk3EV77kdLEnx135AnOUM2tcuwFO_FeXglrM2P4';

// Create and export the Supabase client
export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Helper function to fetch all physicians
export async function fetchPhysicians() {
    const { data, error } = await supabase
        .from('physicians')
        .select('*')
        .order('id', { ascending: true });

    if (error) {
        console.error('❌ Error fetching physicians:', error);
        throw error;
    }

    console.log('✅ Supabase data loaded successfully!');
    console.log(`📊 Total physicians from database: ${data.length}`);

    return data;
}

// Helper function to fetch physician stats
export async function fetchPhysicianStats() {
    const { data, error } = await supabase
        .from('physician_stats')
        .select('*')
        .single();

    if (error) {
        console.error('❌ Error fetching physician stats:', error);
        return null;
    }

    return data;
}
