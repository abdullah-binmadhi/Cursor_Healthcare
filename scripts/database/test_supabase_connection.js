// Test Supabase Connection
import { createClient } from '@supabase/supabase-js';
import * as dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;

console.log('🔍 Testing Supabase Connection...');
console.log('📍 URL:', supabaseUrl);
console.log('🔑 Key:', supabaseKey ? supabaseKey.substring(0, 20) + '...' : 'NOT FOUND');

if (!supabaseUrl || !supabaseKey) {
    console.error('❌ Missing Supabase credentials in .env file');
    process.exit(1);
}

// Create Supabase client
const supabase = createClient(supabaseUrl, supabaseKey);

// Test connection by fetching database info
async function testConnection() {
    try {
        console.log('\n🔌 Attempting to connect to Supabase...');
        
        // Try a simple query to test the connection
        const { data, error } = await supabase
            .from('physicians')
            .select('count')
            .limit(1);
        
        if (error) {
            // If table doesn't exist, that's okay - connection is still working
            if (error.message.includes('does not exist') || 
                error.code === '42P01' || 
                error.code === 'PGRST205' ||
                error.message.includes('not find the table')) {
                console.log('✅ Connection successful!');
                console.log('ℹ️  Note: "physicians" table does not exist yet (this is expected)');
                console.log('📝 Next step: Create the physicians table in Supabase');
                return true;
            } else {
                throw error;
            }
        }
        
        console.log('✅ Connection successful!');
        console.log('✅ Physicians table exists');
        console.log('📊 Data:', data);
        return true;
        
    } catch (error) {
        console.error('❌ Connection failed:', error.message);
        console.error('Full error:', error);
        return false;
    }
}

testConnection()
    .then((success) => {
        if (success) {
            console.log('\n🎉 Supabase is connected and ready!');
        } else {
            console.log('\n❌ Supabase connection failed. Please check your credentials.');
        }
        process.exit(success ? 0 : 1);
    });
