# Supabase Integration Setup Guide

This guide will help you set up Supabase for the Healthcare Website.

## 📋 Prerequisites

- Supabase account (free tier works)
- Node.js installed
- Git repository set up

## 🚀 Setup Steps

### Step 1: Run the SQL Schema

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor** (left sidebar)
3. Click **New Query**
4. Copy the entire contents of `supabase_schema.sql`
5. Paste it into the SQL editor
6. Click **Run** button

This will create:
- `physicians` table with all necessary columns
- Indexes for fast queries
- Row Level Security (RLS) policies
- A `physician_stats` view for analytics

### Step 2: Migrate Data from CSV

Run the migration script to upload all 110 physicians:

```bash
node migrate_to_supabase.js
```

Expected output:
```
🏥 Starting migration to Supabase...
📄 Reading CSV from: ./healthcare-website/physician_registry.csv
📊 Total lines in CSV: 112
✅ Parsed 110 physicians from CSV
📤 Uploading physicians to Supabase...
✅ Uploaded 110/110 physicians
🎉 Migration completed successfully!
```

### Step 3: Verify Data

1. Go to **Table Editor** in Supabase dashboard
2. Select `physicians` table
3. You should see 110 rows
4. Click on any row to see the data

### Step 4: Deploy Website

The website is already updated to use Supabase API:

```bash
git add .
git commit -m "Integrate Supabase database for physicians data"
git push origin main
```

Vercel will automatically rebuild and deploy.

## ✅ What Changed

### Database (Supabase)
- ✅ Physicians data stored in PostgreSQL database
- ✅ Fast indexed queries
- ✅ Row Level Security enabled
- ✅ Public read access for website visitors
- ✅ No more CSV file path issues

### Website Code
- ✅ Now fetches from Supabase REST API
- ✅ No dependency on CSV files
- ✅ Works reliably on Vercel
- ✅ Data can be updated without redeploying

## 🔧 Configuration

API credentials are in `.env` file (not committed to git):
```
SUPABASE_URL=https://pdgumgpjoeojbojacung.supabase.co
SUPABASE_ANON_KEY=[your-key]
```

The website has these credentials hardcoded for client-side access (this is safe for the anon/public key).

## 📊 Database Structure

### Physicians Table
```sql
- id (TEXT, PRIMARY KEY)
- physician_name (TEXT)
- first_name (TEXT)
- last_name (TEXT)
- specialty (TEXT)
- department_id (TEXT)
- hospital (TEXT)
- rating (DECIMAL)
- availability (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### Indexes
- `idx_physicians_specialty`
- `idx_physicians_hospital`
- `idx_physicians_rating`
- `idx_physicians_availability`

## 🎯 Benefits

✅ **Reliability**: No more 404 errors or file path issues
✅ **Performance**: Database queries are indexed and fast
✅ **Scalability**: Can handle thousands of physicians
✅ **Real-time Updates**: Change data without redeploying
✅ **Security**: Row Level Security protects data
✅ **Admin Ready**: Can build admin panel to manage data

## 🔍 Testing

### Local Testing
1. Open browser console (F12)
2. Navigate to Find Doctors page
3. Check for: `✅ Supabase data loaded successfully!`
4. Verify physician count matches database

### Production Testing
1. Visit cursor-healthcare.vercel.app
2. Go to Find Doctors
3. All 110 physicians should load
4. Filters should work correctly

## 🐛 Troubleshooting

### Migration fails
- Check `.env` file has correct credentials
- Verify SQL schema was run first
- Check Supabase project is active

### Website shows error
- Open browser console for details
- Verify Supabase API is accessible
- Check RLS policies allow public read access

### No doctors display
- Run migration script again
- Check `physicians` table has data
- Verify API key is correct

## 📝 Next Steps

1. ✅ Run SQL schema in Supabase
2. ✅ Run migration script
3. ✅ Test locally
4. ✅ Deploy to Vercel
5. 🔄 (Optional) Build admin panel to manage physicians

## 🆘 Support

If you encounter issues:
1. Check browser console for error messages
2. Verify Supabase dashboard shows data
3. Test API directly: https://pdgumgpjoeojbojacung.supabase.co/rest/v1/physicians
4. Check RLS policies are set correctly
