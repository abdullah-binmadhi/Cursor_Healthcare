# Healthcare Website to n8n Webhook Integration

This integration enables your healthcare analytics platform to trigger n8n workflows when users interact with your website, allowing for automated processing, notifications, and extended functionality.

## Overview

The webhook integration captures key user interactions on your healthcare website and sends them to your n8n instance for further processing. This enables you to:

- Track user behavior and analytics
- Send notifications based on user actions
- Automate follow-up workflows
- Integrate with other systems
- Extend healthcare platform functionality

## Setup Instructions

### 1. Configure n8n Webhook

1. In your n8n instance, create a new webhook node
2. Copy the generated webhook URL
3. Update the `WEBHOOK_URL` in the integration script:

```javascript
const N8N_CONFIG = {
  // Replace with your actual n8n webhook URL
  WEBHOOK_URL: "https://your-n8n-instance.com/webhook/healthcare-event",
  // Authentication token if required
  AUTH_TOKEN: "your-webhook-token-here",
  // Timeout for webhook requests (milliseconds)
  TIMEOUT: 5000
};
```

### 2. Add Integration to Healthcare Website

Include the webhook integration script in your healthcare website by adding it to [healthcare-website/index.html](file:///Users/abdullahbinmadhi/Desktop/Cursor_Healthcare/healthcare-website/index.html):

```html
<!-- Add this before the closing </body> tag -->
<script src="scripts/n8n_webhook_integration.js"></script>
```

### 3. Configure n8n Workflow

Create a new workflow in n8n with an HTTP webhook trigger:

1. Add "HTTP Request" trigger node
2. Set the URL to match your webhook endpoint
3. Configure authentication if needed
4. Add nodes to process the incoming data

Example n8n workflow structure:
```
HTTP Webhook Trigger → Function Node (Process Data) → Switch Node (Route by Event Type) → Action Nodes
```

## Supported Events

The integration captures the following events from your healthcare website:

### 1. Patient Search (`patient_search`)
Triggered when users search for doctors or filter by specialty/hospital.

Data sent:
```json
{
  "eventType": "patient_search",
  "eventData": {
    "searchParams": {
      "specialty": "Cardiology",
      "hospital": "City General Hospital"
    },
    "userId": "user_x9z3k2p8q",
    "timestamp": "2025-09-02T10:30:00.000Z"
  }
}
```

### 2. Cost Estimate (`cost_estimate`)
Triggered when users calculate healthcare costs.

Data sent:
```json
{
  "eventType": "cost_estimate",
  "eventData": {
    "estimateData": {
      "patientAge": "45",
      "insuranceType": "private",
      "department": "Surgery",
      "procedure": "major-surgery"
    },
    "userId": "user_x9z3k2p8q",
    "timestamp": "2025-09-02T10:30:00.000Z"
  }
}
```

### 3. Doctor Rating (`doctor_rating`)
Triggered when users view or interact with doctor ratings.

Data sent:
```json
{
  "eventType": "doctor_rating",
  "eventData": {
    "ratingData": {
      "doctorName": "Dr. Sarah Johnson",
      "specialty": "Cardiology",
      "rating": 4.8,
      "hospital": "City General Hospital"
    },
    "userId": "user_x9z3k2p8q",
    "timestamp": "2025-09-02T10:30:00.000Z"
  }
}
```

### 4. Analytics View (`analytics_view`)
Triggered when users access the analytics dashboard.

Data sent:
```json
{
  "eventType": "analytics_view",
  "eventData": {
    "analyticsData": {
      "viewType": "dashboard_access",
      "filters": {
        "year": "2024",
        "hospital": "all"
      }
    },
    "userId": "user_x9z3k2p8q",
    "timestamp": "2025-09-02T10:30:00.000Z"
  }
}
```

## Example n8n Workflows

### 1. User Activity Tracking

```
HTTP Webhook → Set → Google Sheets (Append)
```

Track all user interactions in a Google Sheet for analytics.

### 2. Cost Estimate Notifications

```
HTTP Webhook → Switch (cost_estimate) → Email (Send estimate summary)
```

Send email notifications with cost estimates to users.

### 3. Popular Search Analysis

```
HTTP Webhook → Filter (patient_search) → Function (Aggregate) → Database (Store)
```

Analyze popular doctor/hospital searches to improve recommendations.

## Security Considerations

1. **Authentication**: Use the AUTH_TOKEN to secure your webhook endpoint
2. **Data Privacy**: Only send anonymous user identifiers, not personal information
3. **Rate Limiting**: Implement rate limiting in n8n to prevent abuse
4. **HTTPS**: Ensure your n8n instance uses HTTPS

## Testing

Test the integration using the built-in test function:

```javascript
// In browser console
testN8nWebhook().then(success => {
  console.log('Webhook test result:', success ? 'Success' : 'Failed');
});
```

## Troubleshooting

### Common Issues:

1. **Webhook URL incorrect**: Verify the URL matches your n8n webhook endpoint
2. **Authentication failed**: Check that AUTH_TOKEN is correctly configured
3. **CORS errors**: Ensure your n8n instance allows requests from your website domain
4. **Timeout errors**: Increase TIMEOUT value for slow n8n instances

### Debugging:

1. Check browser console for JavaScript errors
2. Verify network requests in browser developer tools
3. Check n8n execution logs
4. Test webhook URL directly with curl or Postman

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

## Privacy Compliance

The integration is designed to be privacy-compliant:
- Uses anonymous user identifiers
- Does not collect personal health information
- Only tracks user interactions, not personal data
- Follows healthcare data privacy best practices

## Support

For issues with the integration:
1. Verify n8n webhook configuration
2. Check network connectivity
3. Review browser console for errors
4. Ensure healthcare website JavaScript is loading correctly

## Healthcare Analytics Platform Integration

This webhook integration works seamlessly with your Cursor Healthcare Analytics platform, enabling:
- Real-time user behavior tracking
- Automated workflow triggers
- Enhanced analytics capabilities
- Integration with external systems
- Extended platform functionality