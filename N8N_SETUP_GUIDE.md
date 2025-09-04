# How to Connect Healthcare Website to n8n via Webhook

This guide will walk you through the process of connecting your healthcare website to n8n using webhooks to automate workflows based on user interactions.

## Prerequisites

1. An n8n instance (self-hosted or cloud)
2. Access to your healthcare website files
3. Basic understanding of n8n workflows

## Step 1: Set up n8n Webhook

1. Log in to your n8n instance
2. Create a new workflow
3. Add an "HTTP Request" trigger node
4. Configure the trigger:
   - Set the HTTP method to "POST"
   - Copy the generated webhook URL (you'll need this in Step 3)

## Step 2: Configure Healthcare Website Integration

1. Open the n8n integration configuration file:
   ```
   /healthcare-website/scripts/n8n_webhook_integration.js
   ```

2. Update the configuration section with your actual n8n webhook URL:
   ```javascript
   const N8N_CONFIG = {
     // Replace with your actual n8n webhook URL from Step 1
     WEBHOOK_URL: "https://your-n8n-instance.com/webhook/YOUR-WEBHOOK-ID",
     // Authentication token if required (optional)
     AUTH_TOKEN: "",
     // Timeout for webhook requests (milliseconds)
     TIMEOUT: 5000
   };
   ```

3. Save the file

## Step 3: Test the Connection

1. Open your healthcare website in a browser
2. Open the browser's developer console (F12 or right-click → Inspect → Console)
3. Run the test function:
   ```javascript
   testN8nWebhook().then(success => {
     console.log('Webhook test result:', success ? 'Success' : 'Failed');
   });
   ```
4. Check the console for success messages

## Step 4: Create n8n Workflows

The healthcare website sends different types of events to n8n:

### Event Types

1. **Patient Search** (`patient_search`)
   - Triggered when users search for doctors or filter by specialty/hospital
   - Data includes search parameters and anonymous user ID

2. **Cost Estimate** (`cost_estimate`)
   - Triggered when users calculate healthcare costs
   - Data includes patient information and procedure details

3. **Doctor Rating** (`doctor_rating`)
   - Triggered when users view or interact with doctor ratings
   - Data includes doctor information and ratings

4. **Analytics View** (`analytics_view`)
   - Triggered when users access the analytics dashboard
   - Data includes dashboard access information

### Sample n8n Workflow

1. HTTP Request Trigger (configured with your webhook URL)
2. Function Node to process data:
   ```javascript
   // Example: Log the event type
   console.log('Received event:', $json.eventType);
   return $json;
   ```
3. Switch Node to route by event type
4. Action nodes for each event type (email, database, etc.)

## Troubleshooting

### Common Issues

1. **Connection failed**: Verify the webhook URL is correct
2. **Authentication error**: Check that AUTH_TOKEN is properly configured
3. **CORS error**: Ensure your n8n instance allows requests from your website domain
4. **Timeout error**: Increase TIMEOUT value for slow connections

### Debugging Tips

1. Check browser console for JavaScript errors
2. Verify network requests in browser developer tools
3. Check n8n execution logs
4. Test webhook URL directly with curl or Postman

## Security Considerations

1. Use HTTPS for your n8n instance
2. Implement authentication with AUTH_TOKEN if needed
3. Only send anonymous identifiers, not personal health information
4. Consider rate limiting in n8n to prevent abuse

## Customization

You can extend the integration by adding more event types:

```javascript
function onCustomEvent(customData) {
  sendHealthcareEventToN8n('custom_event', {
    customData: customData,
    userId: getAnonymousUserId(),
    timestamp: new Date().toISOString()
  });
}
```

## Support

For issues with the integration:
1. Verify n8n webhook configuration
2. Check network connectivity
3. Review browser console for errors
4. Ensure healthcare website JavaScript is loading correctly