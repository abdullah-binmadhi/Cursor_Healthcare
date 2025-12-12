/**
 * Healthcare Website JavaScript
 * Handles cost estimation and analytics functionality
 * NOTE: Doctor finder now uses Supabase (loaded in index.html inline script)
 */

// Global data storage
let physiciansData = []; // This will be populated from Supabase in index.html
let financialData = [];
let departmentData = [];
let filteredDoctors = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
async function initializeApp() {
    try {
        // Load only CSV data files for analytics (NOT physicians - they come from Supabase)
        await loadDataFiles();
        
        // Set up event listeners
        setupEventListeners();
        
        console.log('✅ Healthcare app initialized (physicians loaded from Supabase)');
    } catch (error) {
        console.error('Error initializing app:', error);
        showError('Failed to load healthcare data. Please refresh the page.');
    }
}

/**
 * Load CSV data files (financial and department data only)
 */
async function loadDataFiles() {
    try {
        const [financial, departments] = await Promise.all([
            loadCSV('data/financial_performance.csv'),
            loadCSV('data/department_metrics.csv')
        ]);
        
        // DO NOT load physicians from CSV - they come from Supabase
        financialData = financial;
        departmentData = departments;
        
        console.log('📊 CSV Data loaded:', {
            financial: financialData.length,
            departments: departmentData.length
        });
        console.log('👨‍⚕️ Physicians: Loaded from Supabase (see index.html inline script)');
    } catch (error) {
        console.error('Error loading CSV files:', error);
        throw error;
    }
}

/**
 * Load CSV file and parse to JSON
 */
async function loadCSV(filePath) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`Failed to load ${filePath}: ${response.statusText}`);
        }
        
        const csvText = await response.text();
        return parseCSV(csvText);
    } catch (error) {
        console.error(`Error loading CSV ${filePath}:`, error);
        // Return empty array as fallback
        return [];
    }
}

/**
 * Parse CSV text to JSON array
 */
function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
    
    return lines.slice(1).map(line => {
        const values = parseCSVLine(line);
        const row = {};
        headers.forEach((header, index) => {
            let value = values[index] || '';
            value = value.replace(/"/g, '').trim();
            
            // Convert numeric values
            if (!isNaN(value) && value !== '') {
                row[header] = parseFloat(value);
            } else {
                row[header] = value;
            }
        });
        return row;
    });
}

/**
 * Parse a single CSV line handling quoted values
 */
function parseCSVLine(line) {
    const values = [];
    let current = '';
    let inQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
        const char = line[i];
        
        if (char === '"') {
            inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
            values.push(current);
            current = '';
        } else {
            current += char;
        }
    }
    
    values.push(current);
    return values;
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    // Cost estimator form
    const costForm = document.getElementById('costEstimatorForm');
    if (costForm) {
        costForm.addEventListener('submit', handleCostEstimation);
    }
    
    // Doctor search filters
    const filters = ['specialtyFilter', 'hospitalFilter', 'ratingFilter', 'availabilityFilter'];
    filters.forEach(filterId => {
        const element = document.getElementById(filterId);
        if (element) {
            element.addEventListener('change', searchDoctors);
        }
    });
}

/**
 * Handle cost estimation form submission
 */
async function handleCostEstimation(event) {
    event.preventDefault();
    
    // Get form values
    const age = parseInt(document.getElementById('patientAge').value);
    const insuranceType = document.getElementById('insuranceType').value;
    const department = document.getElementById('department').value;
    const procedureType = document.getElementById('procedure').value;
    
    // Validate inputs
    if (!age || !insuranceType || !department || !procedureType) {
        showError('Please fill in all fields');
        return;
    }
    
    // Calculate cost estimate
    const estimate = calculateCostEstimate(age, insuranceType, department, procedureType);
    
    // Display results
    displayCostResults(estimate);
}

/**
 * Calculate cost estimate based on user inputs
 */
function calculateCostEstimate(age, insuranceType, department, procedureType) {
    // Find matching financial data
    const matchingData = financialData.filter(item => 
        item.department === department && 
        item.insurance_type === insuranceType && 
        item.procedure_type === procedureType
    );
    
    let baseCost = 2000; // Default base cost
    let insuranceCoverage = 0.7; // Default 70% coverage
    let lengthOfStay = 1; // Default 1 day
    
    if (matchingData.length > 0) {
        const data = matchingData[0];
        baseCost = data.base_cost || baseCost;
        insuranceCoverage = data.insurance_coverage_pct || insuranceCoverage;
        lengthOfStay = data.length_of_stay_days || lengthOfStay;
    }
    
    // Apply age-based adjustments
    let ageMultiplier = 1;
    if (age < 18) ageMultiplier = 0.8;
    else if (age > 65) ageMultiplier = 1.2;
    
    // Apply procedure-based adjustments
    const procedureMultipliers = {
        'consultation': 0.3,
        'diagnostic': 0.6,
        'minor-surgery': 1.0,
        'major-surgery': 2.5,
        'emergency-visit': 1.5,
        'follow-up': 0.4
    };
    
    const procedureMultiplier = procedureMultipliers[procedureType] || 1;
    
    // Calculate final costs
    const adjustedBaseCost = Math.round(baseCost * ageMultiplier * procedureMultiplier);
    const insuranceAmount = Math.round(adjustedBaseCost * insuranceCoverage);
    const patientCost = adjustedBaseCost - insuranceAmount;
    
    // Generate cost factors
    const factors = [];
    if (age < 18) factors.push('Pediatric discount applied');
    if (age > 65) factors.push('Senior care complexity adjustment');
    if (procedureType === 'emergency-visit') factors.push('Emergency department premium');
    if (insuranceType === 'self-pay') factors.push('Self-pay discount available');
    factors.push(`${department} department standard rates`);
    factors.push(`${Math.round(insuranceCoverage * 100)}% insurance coverage`);
    
    return {
        estimatedCost: adjustedBaseCost,
        insuranceCoverage: insuranceAmount,
        patientCost: patientCost,
        lengthOfStay: lengthOfStay,
        factors: factors
    };
}

/**
 * Display cost estimation results
 */
function displayCostResults(estimate) {
    const resultsCard = document.getElementById('costResults');
    const estimatedCostEl = document.getElementById('estimatedCost');
    const insuranceCoverageEl = document.getElementById('insuranceCoverage');
    const patientCostEl = document.getElementById('patientCost');
    const lengthOfStayEl = document.getElementById('lengthOfStay');
    const costFactorsEl = document.getElementById('costFactors');
    
    // Update cost values
    if (estimatedCostEl) estimatedCostEl.textContent = `$${estimate.estimatedCost.toLocaleString()}`;
    if (insuranceCoverageEl) insuranceCoverageEl.textContent = `$${estimate.insuranceCoverage.toLocaleString()}`;
    if (patientCostEl) patientCostEl.textContent = `$${estimate.patientCost.toLocaleString()}`;
    if (lengthOfStayEl) lengthOfStayEl.textContent = `${estimate.lengthOfStay} day${estimate.lengthOfStay !== 1 ? 's' : ''}`;
    
    // Update cost factors
    if (costFactorsEl) {
        costFactorsEl.innerHTML = estimate.factors.map(factor => `<li>${factor}</li>`).join('');
    }
    
    // Show results card
    if (resultsCard) {
        resultsCard.style.display = 'block';
        resultsCard.classList.add('fade-in');
    }
    
    // Scroll to results
    if (resultsCard) {
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

/**
 * ================================================================
 * DOCTOR SEARCH FUNCTIONS DISABLED
 * All doctor/physician functionality now uses Supabase in index.html
 * The following functions are commented out to prevent conflicts:
 * - searchDoctors()
 * - displayDoctors()
 * - createDoctorCard()
 * ================================================================
 */

/* COMMENTED OUT - NOW IN INDEX.HTML WITH SUPABASE
function searchDoctors() { ... }
function displayDoctors(doctors) { ... }
function createDoctorCard(doctor) {
    const card = document.createElement('div');
    card.className = 'doctor-card fade-in';
    
    // Generate star rating
    const rating = doctor.patient_satisfaction || 0;
    const stars = '★'.repeat(Math.floor(rating)) + '☆'.repeat(5 - Math.floor(rating));
    
    // Determine availability class
    ... (doctor card creation code - see index.html for Supabase version) ...
}

function getAvailabilityText(status, waitTime) {
    ... (availability text logic - see index.html for Supabase version) ...
}
END OF COMMENTED OUT SECTION */

// ================================================================
// ACTIVE FUNCTIONS BELOW - These remain active for other features
// ================================================================

/**
 * Utility function to scroll to a section
 */
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Show error message
 */
function showError(message) {
    // Create or update error element
    let errorEl = document.getElementById('error-message');
    if (!errorEl) {
        errorEl = document.createElement('div');
        errorEl.id = 'error-message';
        errorEl.className = 'error';
        document.body.appendChild(errorEl);
    }
    
    errorEl.textContent = message;
    errorEl.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorEl.style.display = 'none';
    }, 5000);
}

/**
 * Show success message
 */
function showSuccess(message) {
    // Create or update success element
    let successEl = document.getElementById('success-message');
    if (!successEl) {
        successEl = document.createElement('div');
        successEl.id = 'success-message';
        successEl.className = 'success';
        document.body.appendChild(successEl);
    }
    
    successEl.textContent = message;
    successEl.style.display = 'block';
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        successEl.style.display = 'none';
    }, 3000);
}

// Export functions for potential external use
window.HealthcareApp = {
    scrollToSection,
    searchDoctors,
    calculateCostEstimate,
    displayDoctors,
    showError,
    showSuccess
};