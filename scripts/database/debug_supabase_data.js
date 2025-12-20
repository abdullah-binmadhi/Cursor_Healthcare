// Debug script to check Supabase data and filter values
import { createClient } from '@supabase/supabase-js';
import * as dotenv from 'dotenv';

dotenv.config();

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function debugData() {
    console.log('🔍 Fetching physicians from Supabase...\n');
    
    const { data: physicians, error } = await supabase
        .from('physicians')
        .select('*')
        .limit(5);
    
    if (error) {
        console.error('❌ Error:', error);
        return;
    }
    
    console.log('📊 Sample physicians:');
    physicians.forEach(p => {
        console.log(`\nID: ${p.id}`);
        console.log(`Name: ${p.first_name} ${p.last_name}`);
        console.log(`Specialty: "${p.specialty}"`);
        console.log(`Hospital: "${p.hospital}"`);
        console.log(`Rating: ${p.rating}`);
        console.log(`Availability: "${p.availability}"`);
    });
    
    // Get unique values
    const { data: allPhysicians } = await supabase
        .from('physicians')
        .select('specialty, hospital, availability');
    
    const specialties = [...new Set(allPhysicians.map(p => p.specialty))].sort();
    const hospitals = [...new Set(allPhysicians.map(p => p.hospital))].sort();
    const availabilities = [...new Set(allPhysicians.map(p => p.availability))].sort();
    
    console.log('\n🏥 Unique Specialties:', specialties);
    console.log('\n🏥 Unique Hospitals:', hospitals);
    console.log('\n📅 Unique Availabilities:', availabilities);
}

debugData();
