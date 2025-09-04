/**
 * Healthcare Website to n8n Webhook Integration
 * This script enables triggering n8n workflows from healthcare website events
 * 
 * Author: Abdullah Bin Madhi
 * Date: 2025-09-02
 */

// Configuration - UPDATE THESE VALUES WITH YOUR ACTUAL n8n WEBHOOK SETTINGS
const N8N_CONFIG = {
  // Replace with your actual n8n webhook URL from your n8n instance
  WEBHOOK_URL: "http://localhost:5678/webhook/1713971d-d977-4988-9efb-9ec8bd234776",
  // Authentication token if required (leave empty if not using authentication)
  AUTH_TOKEN: "",
  // Timeout for webhook requests (milliseconds)
  TIMEOUT: 5000
};

/**
 * Send webhook to n8n when a healthcare event occurs
 * @param {string} eventType - Type of event (e.g., 'patient_search', 'cost_estimate', 'doctor_rating')
 * @param {Object} eventData - Data related to the event
 * @returns {Promise<Object>} Response from n8n
 */
async function sendHealthcareEventToN8n(eventType, eventData) {
  try {
    // Prepare the webhook payload
    const payload = {
      timestamp: new Date().toISOString(),
      eventType: eventType,
      eventData: eventData,
      source: "healthcare-website"
    };

    // Send POST request to n8n webhook
    const response = await fetch(N8N_CONFIG.WEBHOOK_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${N8N_CONFIG.AUTH_TOKEN}`,
        'User-Agent': 'Healthcare-Website-Webhook/1.0'
      },
      body: JSON.stringify(payload),
      timeout: N8N_CONFIG.TIMEOUT
    });

    // Check if request was successful
    if (!response.ok) {
      throw new Error(`n8n webhook request failed with status ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();
    console.log(`Successfully sent ${eventType} event to n8n`);
    return result;
  } catch (error) {
    console.error(`Error sending ${eventType} event to n8n:`, error);
    // Re-throw error for handling by caller
    throw error;
  }
}

/**
 * Trigger n8n workflow when a patient search is performed
 * @param {Object} searchParams - Patient search parameters
 */
function onPatientSearch(searchParams) {
  sendHealthcareEventToN8n('patient_search', {
    searchParams: searchParams,
    userId: getAnonymousUserId(), // Get anonymous user identifier
    timestamp: new Date().toISOString()
  }).catch(error => {
    // Log error but don't block user experience
    console.error('Failed to send patient search event to n8n:', error);
  });
}

/**
 * Trigger n8n workflow when a cost estimate is calculated
 * @param {Object} estimateData - Cost estimation data
 */
function onCostEstimate(estimateData) {
  sendHealthcareEventToN8n('cost_estimate', {
    estimateData: estimateData,
    userId: getAnonymousUserId(),
    timestamp: new Date().toISOString()
  }).catch(error => {
    console.error('Failed to send cost estimate event to n8n:', error);
  });
}

/**
 * Trigger n8n workflow when a doctor is rated
 * @param {Object} ratingData - Doctor rating data
 */
function onDoctorRating(ratingData) {
  sendHealthcareEventToN8n('doctor_rating', {
    ratingData: ratingData,
    userId: getAnonymousUserId(),
    timestamp: new Date().toISOString()
  }).catch(error => {
    console.error('Failed to send doctor rating event to n8n:', error);
  });
}

/**
 * Trigger n8n workflow when analytics data is viewed
 * @param {Object} analyticsData - Analytics view data
 */
function onAnalyticsView(analyticsData) {
  sendHealthcareEventToN8n('analytics_view', {
    analyticsData: analyticsData,
    userId: getAnonymousUserId(),
    timestamp: new Date().toISOString()
  }).catch(error => {
    console.error('Failed to send analytics view event to n8n:', error);
  });
}

/**
 * Generate an anonymous user identifier for tracking
 * This preserves privacy while allowing basic usage analytics
 * @returns {string} Anonymous user ID
 */
function getAnonymousUserId() {
  // Check if we already have a user ID stored
  let userId = localStorage.getItem('anonymousUserId');
  
  if (!userId) {
    // Generate a new anonymous user ID
    userId = 'user_' + Math.random().toString(36).substr(2, 9);
    // Store it for future use
    localStorage.setItem('anonymousUserId', userId);
  }
  
  return userId;
}

/**
 * Initialize webhook integration
 */
function initializeWebhookIntegration() {
  console.log('Initializing n8n webhook integration for healthcare website');
  
  // Add event listeners for healthcare website events
  setupHealthcareEventListeners();
  
  console.log('n8n webhook integration initialized successfully');
}

/**
 * Set up event listeners for healthcare website events
 */
function setupHealthcareEventListeners() {
  // Listen for form submissions on the cost estimator
  const costEstimatorForm = document.getElementById('costEstimatorForm');
  if (costEstimatorForm) {
    costEstimatorForm.addEventListener('submit', function(event) {
      // Prevent default to handle after data collection
      event.preventDefault();
      
      // Get form data
      const formData = new FormData(costEstimatorForm);
      const estimateData = {
        patientAge: formData.get('patientAge'),
        insuranceType: formData.get('insuranceType'),
        department: formData.get('department'),
        procedure: formData.get('procedure')
      };
      
      // Send to n8n
      onCostEstimate(estimateData);
      
      // Continue with form submission
      costEstimatorForm.submit();
    });
  }
  
  // Listen for doctor search events
  const specialtyFilter = document.getElementById('specialtyFilter');
  const hospitalFilter = document.getElementById('hospitalFilter');
  
  if (specialtyFilter) {
    specialtyFilter.addEventListener('change', function() {
      onPatientSearch({
        specialty: specialtyFilter.value,
        hospital: hospitalFilter ? hospitalFilter.value : null
      });
    });
  }
  
  if (hospitalFilter) {
    hospitalFilter.addEventListener('change', function() {
      onPatientSearch({
        hospital: hospitalFilter.value,
        specialty: specialtyFilter ? specialtyFilter.value : null
      });
    });
  }
  
  // Listen for analytics dashboard views
  const analyticsSection = document.getElementById('analytics');
  if (analyticsSection) {
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
          if (analyticsSection.classList.contains('active')) {
            onAnalyticsView({
              viewType: 'dashboard_access',
              filters: {
                year: document.querySelector('.year-tab.active')?.dataset.year || '2024',
                hospital: document.getElementById('hospitalSelector')?.value || 'all'
              },
              timestamp: new Date().toISOString()
            });
          }
        }
      });
    });
    
    observer.observe(analyticsSection, {
      attributes: true,
      attributeFilter: ['class']
    });
  }
  
  // Listen for doctor card interactions (ratings)
  document.addEventListener('click', function(event) {
    // Check if a doctor card rating element was clicked
    const ratingElement = event.target.closest('.doctor-rating');
    if (ratingElement) {
      const doctorCard = event.target.closest('.doctor-card');
      if (doctorCard) {
        const doctorName = doctorCard.querySelector('.doctor-name')?.textContent || 'Unknown';
        const specialty = doctorCard.querySelector('.doctor-specialty')?.textContent || 'Unknown';
        const rating = ratingElement.textContent.trim();
        const hospital = doctorCard.querySelector('.doctor-details')?.textContent || 'Unknown';
        
        onDoctorRating({
          doctorName: doctorName,
          specialty: specialty,
          rating: parseFloat(rating) || 0,
          hospital: hospital
        });
      }
    }
  });
}

/**
 * Test function to verify n8n webhook connectivity
 */
async function testN8nWebhook() {
  try {
    console.log('Testing n8n webhook connectivity...');
    
    const testResult = await sendHealthcareEventToN8n('test_connection', {
      message: 'Healthcare website n8n webhook test',
      timestamp: new Date().toISOString()
    });
    
    console.log('n8n webhook test successful:', testResult);
    return true;
  } catch (error) {
    console.error('n8n webhook test failed:', error);
    return false;
  }
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeWebhookIntegration);
} else {
  initializeWebhookIntegration();
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    sendHealthcareEventToN8n,
    onPatientSearch,
    onCostEstimate,
    onDoctorRating,
    onAnalyticsView,
    testN8nWebhook
  };
}