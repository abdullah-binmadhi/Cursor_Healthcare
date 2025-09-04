# Advanced Healthcare Website Events Workflow Setup Guide

This guide will help you set up the advanced n8n workflow that includes database storage, Slack notifications, data analysis, and user segmentation.

## Prerequisites

1. n8n instance (local or cloud)
2. PostgreSQL database
3. Slack workspace (optional)
4. Google Sheets (optional)

## Step 1: Database Setup

1. Execute the database schema script:
   ```bash
   psql -U your_username -d your_database -f healthcare_events_database.sql
   ```

2. Note your database connection details:
   - Host
   - Port
   - Database name
   - Username
   - Password

## Step 2: Import the Workflow

1. In n8n, go to Workflows
2. Click "+" and select "Import from JSON"
3. Upload [Advanced_Healthcare_Website_Events_Workflow.json](file:///Users/abdullahbinmadhi/Desktop/Cursor_Healthcare/Advanced_Healthcare_Website_Events_Workflow.json)
4. Click "Import"

## Step 3: Configure Database Node

1. Click on the "Store in PostgreSQL" node
2. Click "Select a credential" or "Create new"
3. Enter your PostgreSQL connection details:
   - Host
   - Port
   - Database
   - User
   - Password
4. Test the connection and save

## Step 4: Configure Slack (Optional)

1. Click on any Slack node
2. Click "Select a credential" or "Create new"
3. Follow n8n's OAuth flow to connect to Slack
4. Update channel names as needed:
   - `#healthcare-notifications` for general events
   - `#healthcare-analytics` for analysis reports
   - `#healthcare-sales` for high-value user alerts

## Step 5: Configure Google Sheets (Optional)

1. Click on the "Log to Google Sheets" node
2. Replace `YOUR_GOOGLE_SHEET_ID` with your actual Google Sheet ID
3. Configure Google Sheets credentials through OAuth

## Step 6: Test the Workflow

1. Toggle the workflow to "Active"
2. Go to your healthcare website
3. Navigate to [/healthcare-website/n8n_test.html](file:///Users/abdullahbinmadhi/Desktop/Cursor_Healthcare/healthcare-website/n8n_test.html)
4. Click "Test Connection"
5. Check n8n execution log for success
6. Verify data appears in your database:
   ```sql
   SELECT * FROM healthcare_events ORDER BY timestamp DESC LIMIT 5;
   ```

## Workflow Features Explained

### 1. Database Storage
- All events are stored in PostgreSQL with full JSON data
- Indexes for fast querying by event type, user ID, and timestamp
- Automatic timestamp updates

### 2. User Segmentation
Four user types are identified:
- **regular**: Standard users
- **high_value**: Users interested in major procedures
- **power_user**: Frequent analytics dashboard users
- **engaged**: Users who give high ratings

### 3. Real-time Notifications
- Slack alerts for all events
- Special handling for high-value users
- Daily analysis reports

### 4. Behavior Analysis
- Daily summary of user activities
- Event distribution analysis
- User engagement metrics
- Performance analytics materialized view

## Customization Options

### Add More User Types
Modify the "Process & Segment Users" code node to add new segmentation logic.

### Add More Event Types
The workflow handles the four standard event types:
- patient_search
- cost_estimate
- doctor_rating
- analytics_view

You can extend this by adding more cases to the switch statement.

### Modify Analysis
Update the "Behavior Analysis" code node to include additional metrics.

## Monitoring Queries

Use these SQL queries to monitor your system:

```sql
-- Recent events
SELECT * FROM healthcare_events ORDER BY timestamp DESC LIMIT 10;

-- Daily event counts
SELECT DATE(timestamp) as date, COUNT(*) as events 
FROM healthcare_events 
GROUP BY DATE(timestamp) 
ORDER BY date DESC;

-- User type distribution
SELECT user_type, COUNT(*) as count 
FROM healthcare_events 
GROUP BY user_type 
ORDER BY count DESC;

-- High-value users
SELECT user_id, COUNT(*) as major_procedure_interest 
FROM healthcare_events 
WHERE event_data->>'procedure' = 'major-surgery' 
GROUP BY user_id 
ORDER BY major_procedure_interest DESC;
```

## Troubleshooting

### Database Connection Issues
1. Verify PostgreSQL is running
2. Check connection credentials
3. Ensure firewall allows connections
4. Verify database user has proper permissions

### Slack Notifications Not Working
1. Check OAuth token validity
2. Verify bot has access to channels
3. Confirm channel names exist

### Events Not Being Processed
1. Check webhook URL matches your healthcare website config
2. Verify workflow is active
3. Check n8n execution logs for errors

## Security Considerations

1. Use strong database passwords
2. Limit database user permissions to only what's needed
3. Rotate API keys regularly
4. Use HTTPS for all webhooks
5. Consider adding authentication to your webhook endpoint

## Performance Optimization

1. Regularly refresh the materialized view:
   ```sql
   REFRESH MATERIALIZED VIEW event_performance_analytics;
   ```

2. Monitor database size and archive old events if needed

3. Consider partitioning the events table by date for large datasets

## Integration with Existing Systems

You can extend this workflow to:
1. Send data to your existing analytics platform
2. Integrate with CRM systems
3. Trigger email campaigns
4. Update user profiles in other systems

The JSON structure makes it easy to transform data for other systems.