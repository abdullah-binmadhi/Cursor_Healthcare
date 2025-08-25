/**
 * Healthcare Analytics Dashboard JavaScript - Version 2.3-FINAL
 * Enhanced Charts with Smart Color Coding & Professional Design
 * CHART FIXES: Accurate Revenue & Occupancy Data Display
 * DEPLOYMENT: 2025-08-25 16:45 UTC - CACHE BUST FORCED
 * Last Updated: 2025-08-25 16:45 - Department Chart Data Fixed
 * Handles interactive dashboards, charts, and KPI calculations
 */

// CACHE BUSTER - Force fresh load
console.log('🚀 DASHBOARD LOADING - Version 2.3-FINAL - Chart Fixes Active!');
console.log('⚡ Cache timestamp:', new Date().toISOString());

// Global variables
let dashboardData = {
    physicians: [],
    financial: [],
    departments: [],
    demographics: []
};

let chartInstances = {};
let isInitialized = false;
let currentDashboard = null;
let currentTrendsYear = 2024; // Track current year for trends chart

// Comprehensive year-based healthcare data for synchronized dashboard updates
const healthcareDataByYear = {
    2024: {
        departments: [
            { department_name: 'Cardiology', patient_satisfaction: 4.2, current_occupancy: 0.85, total_patients: 1250, average_cost: 8500, quality_score: 92 },
            { department_name: 'Emergency', patient_satisfaction: 3.8, current_occupancy: 0.92, total_patients: 2100, average_cost: 3200, quality_score: 87 },
            { department_name: 'Surgery', patient_satisfaction: 4.5, current_occupancy: 0.78, total_patients: 890, average_cost: 12500, quality_score: 95 },
            { department_name: 'Orthopedics', patient_satisfaction: 4.3, current_occupancy: 0.72, total_patients: 680, average_cost: 9800, quality_score: 90 },
            { department_name: 'Neurology', patient_satisfaction: 4.1, current_occupancy: 0.65, total_patients: 450, average_cost: 11200, quality_score: 88 },
            { department_name: 'Pediatrics', patient_satisfaction: 4.6, current_occupancy: 0.58, total_patients: 720, average_cost: 4500, quality_score: 93 },
            { department_name: 'Oncology', patient_satisfaction: 4.4, current_occupancy: 0.82, total_patients: 380, average_cost: 15800, quality_score: 91 }
        ],
        physicians: [
            { first_name: 'Sarah', last_name: 'Johnson', specialty: 'Cardiology', patient_satisfaction: 4.8, success_rate: 96, total_patients: 420 },
            { first_name: 'Michael', last_name: 'Chen', specialty: 'Surgery', patient_satisfaction: 4.7, success_rate: 98, total_patients: 380 },
            { first_name: 'Emily', last_name: 'Rodriguez', specialty: 'Pediatrics', patient_satisfaction: 4.9, success_rate: 97, total_patients: 350 },
            { first_name: 'David', last_name: 'Thompson', specialty: 'Emergency', patient_satisfaction: 4.5, success_rate: 94, total_patients: 650 },
            { first_name: 'Lisa', last_name: 'Park', specialty: 'Oncology', patient_satisfaction: 4.6, success_rate: 95, total_patients: 280 },
            { first_name: 'Robert', last_name: 'Williams', specialty: 'Cardiology', patient_satisfaction: 4.4, success_rate: 93, total_patients: 390 },
            { first_name: 'Jennifer', last_name: 'Davis', specialty: 'Surgery', patient_satisfaction: 4.6, success_rate: 96, total_patients: 320 },
            { first_name: 'James', last_name: 'Miller', specialty: 'Orthopedics', patient_satisfaction: 4.3, success_rate: 92, total_patients: 310 },
            { first_name: 'Maria', last_name: 'Garcia', specialty: 'Neurology', patient_satisfaction: 4.5, success_rate: 94, total_patients: 270 },
            { first_name: 'Christopher', last_name: 'Brown', specialty: 'Emergency', patient_satisfaction: 4.2, success_rate: 91, total_patients: 580 },
            { first_name: 'Amanda', last_name: 'Wilson', specialty: 'Pediatrics', patient_satisfaction: 4.7, success_rate: 95, total_patients: 330 },
            { first_name: 'Kevin', last_name: 'Taylor', specialty: 'Oncology', patient_satisfaction: 4.4, success_rate: 93, total_patients: 250 }
        ],
        qualityMetrics: {
            patientSafety: 94,
            clinicalExcellence: 91,
            patientExperience: 88,
            efficiency: 89,
            outcomes: 92,
            innovation: 85
        }
    },
    2023: {
        departments: [
            { department_name: 'Cardiology', patient_satisfaction: 4.0, current_occupancy: 0.82, total_patients: 1180, average_cost: 8200, quality_score: 89 },
            { department_name: 'Emergency', patient_satisfaction: 3.6, current_occupancy: 0.89, total_patients: 1980, average_cost: 3100, quality_score: 84 },
            { department_name: 'Surgery', patient_satisfaction: 4.3, current_occupancy: 0.75, total_patients: 820, average_cost: 12000, quality_score: 92 },
            { department_name: 'Orthopedics', patient_satisfaction: 4.1, current_occupancy: 0.69, total_patients: 630, average_cost: 9500, quality_score: 87 },
            { department_name: 'Neurology', patient_satisfaction: 3.9, current_occupancy: 0.62, total_patients: 410, average_cost: 10800, quality_score: 85 },
            { department_name: 'Pediatrics', patient_satisfaction: 4.4, current_occupancy: 0.55, total_patients: 680, average_cost: 4300, quality_score: 90 },
            { department_name: 'Oncology', patient_satisfaction: 4.2, current_occupancy: 0.79, total_patients: 350, average_cost: 15200, quality_score: 88 }
        ],
        physicians: [
            { first_name: 'Sarah', last_name: 'Johnson', specialty: 'Cardiology', patient_satisfaction: 4.6, success_rate: 94, total_patients: 390 },
            { first_name: 'Michael', last_name: 'Chen', specialty: 'Surgery', patient_satisfaction: 4.5, success_rate: 96, total_patients: 360 },
            { first_name: 'Emily', last_name: 'Rodriguez', specialty: 'Pediatrics', patient_satisfaction: 4.7, success_rate: 95, total_patients: 320 },
            { first_name: 'David', last_name: 'Thompson', specialty: 'Emergency', patient_satisfaction: 4.3, success_rate: 92, total_patients: 620 },
            { first_name: 'Lisa', last_name: 'Park', specialty: 'Oncology', patient_satisfaction: 4.4, success_rate: 93, total_patients: 260 },
            { first_name: 'Robert', last_name: 'Williams', specialty: 'Cardiology', patient_satisfaction: 4.2, success_rate: 91, total_patients: 370 },
            { first_name: 'Jennifer', last_name: 'Davis', specialty: 'Surgery', patient_satisfaction: 4.4, success_rate: 94, total_patients: 300 },
            { first_name: 'James', last_name: 'Miller', specialty: 'Orthopedics', patient_satisfaction: 4.1, success_rate: 90, total_patients: 290 },
            { first_name: 'Maria', last_name: 'Garcia', specialty: 'Neurology', patient_satisfaction: 4.3, success_rate: 92, total_patients: 250 },
            { first_name: 'Christopher', last_name: 'Brown', specialty: 'Emergency', patient_satisfaction: 4.0, success_rate: 89, total_patients: 560 },
            { first_name: 'Amanda', last_name: 'Wilson', specialty: 'Pediatrics', patient_satisfaction: 4.5, success_rate: 93, total_patients: 310 },
            { first_name: 'Kevin', last_name: 'Taylor', specialty: 'Oncology', patient_satisfaction: 4.2, success_rate: 91, total_patients: 230 }
        ],
        qualityMetrics: {
            patientSafety: 91,
            clinicalExcellence: 88,
            patientExperience: 85,
            efficiency: 86,
            outcomes: 89,
            innovation: 82
        }
    },
    2022: {
        departments: [
            { department_name: 'Cardiology', patient_satisfaction: 3.8, current_occupancy: 0.79, total_patients: 1120, average_cost: 7900, quality_score: 86 },
            { department_name: 'Emergency', patient_satisfaction: 3.4, current_occupancy: 0.86, total_patients: 1850, average_cost: 2900, quality_score: 81 },
            { department_name: 'Surgery', patient_satisfaction: 4.1, current_occupancy: 0.72, total_patients: 750, average_cost: 11500, quality_score: 89 },
            { department_name: 'Orthopedics', patient_satisfaction: 3.9, current_occupancy: 0.66, total_patients: 580, average_cost: 9200, quality_score: 84 },
            { department_name: 'Neurology', patient_satisfaction: 3.7, current_occupancy: 0.59, total_patients: 370, average_cost: 10400, quality_score: 82 },
            { department_name: 'Pediatrics', patient_satisfaction: 4.2, current_occupancy: 0.52, total_patients: 640, average_cost: 4100, quality_score: 87 },
            { department_name: 'Oncology', patient_satisfaction: 4.0, current_occupancy: 0.76, total_patients: 320, average_cost: 14800, quality_score: 85 }
        ],
        physicians: [
            { first_name: 'Sarah', last_name: 'Johnson', specialty: 'Cardiology', patient_satisfaction: 4.4, success_rate: 92, total_patients: 360 },
            { first_name: 'Michael', last_name: 'Chen', specialty: 'Surgery', patient_satisfaction: 4.3, success_rate: 94, total_patients: 340 },
            { first_name: 'Emily', last_name: 'Rodriguez', specialty: 'Pediatrics', patient_satisfaction: 4.5, success_rate: 93, total_patients: 290 },
            { first_name: 'David', last_name: 'Thompson', specialty: 'Emergency', patient_satisfaction: 4.1, success_rate: 90, total_patients: 580 },
            { first_name: 'Lisa', last_name: 'Park', specialty: 'Oncology', patient_satisfaction: 4.2, success_rate: 91, total_patients: 240 },
            { first_name: 'Robert', last_name: 'Williams', specialty: 'Cardiology', patient_satisfaction: 4.0, success_rate: 89, total_patients: 350 },
            { first_name: 'Jennifer', last_name: 'Davis', specialty: 'Surgery', patient_satisfaction: 4.2, success_rate: 92, total_patients: 280 },
            { first_name: 'James', last_name: 'Miller', specialty: 'Orthopedics', patient_satisfaction: 3.9, success_rate: 88, total_patients: 270 },
            { first_name: 'Maria', last_name: 'Garcia', specialty: 'Neurology', patient_satisfaction: 4.1, success_rate: 90, total_patients: 230 },
            { first_name: 'Christopher', last_name: 'Brown', specialty: 'Emergency', patient_satisfaction: 3.8, success_rate: 87, total_patients: 540 },
            { first_name: 'Amanda', last_name: 'Wilson', specialty: 'Pediatrics', patient_satisfaction: 4.3, success_rate: 91, total_patients: 280 },
            { first_name: 'Kevin', last_name: 'Taylor', specialty: 'Oncology', patient_satisfaction: 4.0, success_rate: 89, total_patients: 210 }
        ],
        qualityMetrics: {
            patientSafety: 88,
            clinicalExcellence: 85,
            patientExperience: 82,
            efficiency: 83,
            outcomes: 86,
            innovation: 79
        }
    }
};

// Performance optimization: Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎨 Healthcare Dashboard v2.1 - Enhanced Charts Loading...');
    initializeDashboard();
});

/**
 * Initialize the dashboard application
 */
async function initializeDashboard() {
    try {
        console.log('Starting dashboard initialization...');
        
        // Show loading state
        showLoadingState();
        
        // Load data
        await loadDashboardData();
        console.log('Data loaded successfully:', dashboardData);
        
        // Validate data
        if (!dashboardData.physicians || dashboardData.physicians.length === 0) {
            throw new Error('No physician data loaded');
        }
        
        // Setup event listeners
        setupDashboardListeners();
        
        // Initialize the first dashboard
        showDashboard('hospital');
        
        // Hide loading state
        hideLoadingState();
        
        console.log('Dashboard initialized successfully');
    } catch (error) {
        console.error('Error initializing dashboard:', error);
        showError('Failed to load dashboard data. Please refresh the page.');
        hideLoadingState();
    }
}

/**
 * Load all dashboard data
 */
async function loadDashboardData() {
    try {
        console.log('Loading dashboard data...');
        
        const [physicians, financial, departments, demographics] = await Promise.all([
            loadCSV('data/physician_performance.csv'),
            loadCSV('data/financial_performance.csv'),
            loadCSV('data/department_metrics.csv'),
            loadCSV('data/patient_demographics.csv')
        ]);
        
        dashboardData = { physicians, financial, departments, demographics };
        
        console.log('Data loaded:', {
            physicians: physicians.length,
            financial: financial.length,
            departments: departments.length,
            demographics: demographics.length
        });
        
        // Validate data
        if (!physicians.length) throw new Error('No physician data');
        if (!financial.length) throw new Error('No financial data');
        if (!departments.length) throw new Error('No department data');
        if (!demographics.length) throw new Error('No demographics data');
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        throw error;
    }
}

/**
 * Setup dashboard event listeners
 */
function setupDashboardListeners() {
    // Dashboard tab switching
    document.querySelectorAll('.dashboard-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            const dashboardType = this.dataset.dashboard;
            showDashboard(dashboardType);
        });
    });
    
    // Performance metric selector
    const performanceMetric = document.getElementById('performanceMetric');
    if (performanceMetric) {
        performanceMetric.addEventListener('change', updateDepartmentChart);
    }
}

/**
 * Show specific dashboard with performance optimization
 */
function showDashboard(type) {
    // Prevent unnecessary re-renders
    if (currentDashboard === type && isInitialized) {
        return;
    }
    
    currentDashboard = type;
    
    // Update active tab
    document.querySelectorAll('.dashboard-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`[data-dashboard="${type}"]`).classList.add('active');
    
    // Show dashboard section
    document.querySelectorAll('.dashboard-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(`${type}-dashboard`).classList.add('active');
    
    // Lazy load dashboard data with debouncing
    const debouncedLoad = debounce(() => {
        switch(type) {
            case 'hospital': loadHospitalDashboard(); break;
            case 'financial': loadFinancialDashboard(); break;
            case 'patient': loadPatientDashboard(); break;
            case 'physician': loadPhysicianDashboard(); break;
        }
        isInitialized = true;
    }, 150); // 150ms debounce
    
    debouncedLoad();
}

/**
 * Load Hospital Performance Dashboard
 */
function loadHospitalDashboard() {
    console.log('Loading hospital dashboard...');
    
    // Use realistic financial data based on actual healthcare metrics
    const departments = dashboardData.departments.length > 0 ? dashboardData.departments : [
        { department_name: 'Cardiology', patient_satisfaction: 4.2, current_occupancy: 0.85, total_patients: 1250, average_cost: 8500 },
        { department_name: 'Emergency', patient_satisfaction: 3.8, current_occupancy: 0.92, total_patients: 2100, average_cost: 3200 },
        { department_name: 'Surgery', patient_satisfaction: 4.5, current_occupancy: 0.78, total_patients: 890, average_cost: 12500 },
        { department_name: 'Orthopedics', patient_satisfaction: 4.3, current_occupancy: 0.72, total_patients: 680, average_cost: 9800 },
        { department_name: 'Neurology', patient_satisfaction: 4.1, current_occupancy: 0.65, total_patients: 450, average_cost: 11200 },
        { department_name: 'Pediatrics', patient_satisfaction: 4.6, current_occupancy: 0.58, total_patients: 720, average_cost: 4500 },
        { department_name: 'Oncology', patient_satisfaction: 4.4, current_occupancy: 0.82, total_patients: 380, average_cost: 15800 }
    ];
    
    // Calculate realistic financial data
    const financial = departments.map(dept => ({
        total_revenue: dept.total_patients * dept.average_cost,
        department: dept.department_name
    }));
    
    // Calculate KPIs with more realistic numbers
    const totalRevenue = financial.reduce((sum, item) => sum + (item.total_revenue || 0), 0);
    const avgSatisfaction = departments.reduce((sum, dept) => sum + (dept.patient_satisfaction || 0), 0) / departments.length;
    const avgOccupancy = departments.reduce((sum, dept) => sum + (dept.current_occupancy || 0), 0) / departments.length * 100;
    const qualityScore = avgSatisfaction * 20; // Scale to 100
    
    // Update KPI values with improved formatting
    updateElement('totalRevenue', formatCurrency(totalRevenue));
    updateElement('avgSatisfaction', avgSatisfaction.toFixed(1) + '/5.0');
    updateElement('occupancyRate', avgOccupancy.toFixed(1) + '%');
    updateElement('qualityScore', qualityScore.toFixed(1) + '/100');
    
    // Store data for chart creation
    dashboardData.calculatedFinancial = financial;
    dashboardData.calculatedDepartments = departments;
    
    // Create charts with available data - Performance optimized
    requestAnimationFrame(() => {
        setTimeout(() => {
            createDepartmentChart(currentTrendsYear);
            createTrendsChart(currentTrendsYear);
            createQualityChart(currentTrendsYear);
            createHospitalChart();
        }, 50); // Reduced timeout for better responsiveness
    });
}

/**
 * Load Financial Analytics Dashboard
 */
function loadFinancialDashboard() {
    console.log('Loading financial dashboard...');
    
    // Calculate realistic financial metrics from hospital data
    const departments = dashboardData.calculatedDepartments || [
        { department_name: 'Cardiology', total_patients: 1250, average_cost: 8500 },
        { department_name: 'Emergency', total_patients: 2100, average_cost: 3200 },
        { department_name: 'Surgery', total_patients: 890, average_cost: 12500 },
        { department_name: 'Orthopedics', total_patients: 680, average_cost: 9800 },
        { department_name: 'Neurology', total_patients: 450, average_cost: 11200 },
        { department_name: 'Pediatrics', total_patients: 720, average_cost: 4500 },
        { department_name: 'Oncology', total_patients: 380, average_cost: 15800 }
    ];
    
    // Calculate financial KPIs
    const totalRevenue = departments.reduce((sum, dept) => sum + (dept.total_patients * dept.average_cost), 0);
    const totalPatients = departments.reduce((sum, dept) => sum + dept.total_patients, 0);
    const revenuePerPatient = totalPatients > 0 ? totalRevenue / totalPatients : 0;
    const operatingCosts = totalRevenue * 0.82; // 82% cost ratio typical for hospitals
    const operatingMargin = ((totalRevenue - operatingCosts) / totalRevenue) * 100;
    
    // Update financial KPIs with proper formatting
    updateElement('operatingMargin', operatingMargin.toFixed(1) + '%');
    updateElement('revenuePerPatient', formatCurrency(revenuePerPatient));
    updateElement('badDebtRate', '3.2%'); // Industry standard
    updateElement('collectionRate', '94.8%'); // Industry standard
    
    // Store calculated data for charts
    dashboardData.financialCalculated = {
        totalRevenue,
        departments,
        operatingMargin,
        revenuePerPatient
    };
    
    // Create financial charts with delay
    setTimeout(() => {
        createRevenueByDeptChart();
        createRevenueByInsuranceChart();
        createProfitabilityChart();
        createCostBreakdownChart();
    }, 100);
}

/**
 * Load Patient Insights Dashboard
 */
function loadPatientDashboard() {
    const totalPatients = dashboardData.demographics.reduce((sum, item) => sum + (item.patient_count || 0), 0);
    const avgLOS = calculateAverage(dashboardData.departments, 'average_length_stay');
    const avgReadmission = calculateAverage(dashboardData.departments, 'readmission_rate');
    const avgSatisfaction = calculateAverage(dashboardData.demographics, 'satisfaction_score');
    
    updateElement('totalPatients', totalPatients.toLocaleString());
    updateElement('avgLengthOfStay', avgLOS.toFixed(1) + ' days');
    updateElement('readmissionRate', avgReadmission.toFixed(1) + '%');
    updateElement('patientSatisfaction', avgSatisfaction.toFixed(1) + '/5');
    
    // Create patient charts
    createDemographicsChart();
    createInsuranceDistChart();
    createLOSPatternChart();
    createRiskAssessmentChart();
}

/**
 * Load Physician Performance Dashboard
 */
function loadPhysicianDashboard() {
    console.log('Loading physician dashboard...');
    
    // Use fallback data if CSV data isn't available
    const physicians = dashboardData.physicians.length > 0 ? dashboardData.physicians : [
        { first_name: 'John', last_name: 'Smith', patient_satisfaction: 4.5, success_rate: 95, availability_status: 'Available' },
        { first_name: 'Jane', last_name: 'Doe', patient_satisfaction: 4.2, success_rate: 92, availability_status: 'Available' },
        { first_name: 'Mike', last_name: 'Johnson', patient_satisfaction: 4.7, success_rate: 97, availability_status: 'Limited' }
    ];
    
    const activePhysicians = physicians.filter(p => p.availability_status !== 'Unavailable').length;
    const avgPerformance = physicians.reduce((sum, p) => sum + (p.patient_satisfaction || 0), 0) / physicians.length;
    const avgSuccessRate = physicians.reduce((sum, p) => sum + (p.success_rate || 0), 0) / physicians.length;
    const topPerformer = physicians.reduce((max, p) => (p.patient_satisfaction || 0) > (max.patient_satisfaction || 0) ? p : max, physicians[0]);
    
    updateElement('activePhysicians', activePhysicians);
    updateElement('avgPerformance', avgPerformance.toFixed(1) + '/5.0');
    updateElement('avgSuccessRate', avgSuccessRate.toFixed(1) + '%');
    updateElement('topPerformer', `Dr. ${topPerformer?.first_name || 'John'} ${topPerformer?.last_name || 'Smith'}`);
    
    // Create physician charts with delay to ensure DOM is ready
    setTimeout(() => {
        const selectedSpecialty = document.getElementById('physicianSpecialty')?.value || 'all';
        createTopPhysiciansChart(currentTrendsYear, selectedSpecialty);
        createSpecialtyPerformanceChart();
        createWorkloadChart();
        createPhysicianQualityChart();
    }, 100);
}

/**
 * Chart creation functions with enhanced design and clarity
 */
function createDepartmentChart(selectedYear = 2024) {
    const ctx = document.getElementById('departmentChart');
    if (!ctx) return;
    
    // Use year-specific department data
    const departments = healthcareDataByYear[selectedYear]?.departments || healthcareDataByYear[2024].departments;
    
    // Get the selected metric from dropdown
    const metric = document.getElementById('performanceMetric')?.value || 'satisfaction';
    
    let data, label, color, maxValue, formatter, unit;
    
    switch(metric) {
        case 'satisfaction':
            data = departments.map(d => d.patient_satisfaction || 0);
            label = 'Patient Satisfaction Score';
            color = [
                'rgba(72, 187, 120, 0.9)',   // High satisfaction - Green
                'rgba(245, 101, 101, 0.9)',  // Low satisfaction - Red
                'rgba(72, 187, 120, 0.9)',   // High satisfaction - Green
                'rgba(66, 153, 225, 0.9)',   // Medium satisfaction - Blue
                'rgba(139, 92, 246, 0.9)',   // Medium satisfaction - Purple
                'rgba(72, 187, 120, 0.9)',   // High satisfaction - Green
                'rgba(66, 153, 225, 0.9)'    // Medium satisfaction - Blue
            ];
            maxValue = 5;
            formatter = (value) => value.toFixed(1) + '/5';
            unit = '/5';
            break;
        case 'revenue':
            // Calculate accurate revenue with proper scaling
            data = departments.map(d => {
                const revenue = (d.total_patients * d.average_cost) / 1000000; // Convert to millions
                return Math.round(revenue * 10) / 10; // Round to 1 decimal place
            });
            label = 'Revenue (Millions USD)';
            color = departments.map((d, i) => {
                const revenue = data[i];
                if (revenue >= 15) return 'rgba(34, 197, 94, 0.9)';  // High revenue - Green (Oncology: 6.0M)
                if (revenue >= 10) return 'rgba(66, 153, 225, 0.9)';  // High-medium revenue - Blue (Surgery: 11.1M)
                if (revenue >= 6) return 'rgba(139, 92, 246, 0.9)';   // Medium revenue - Purple (Cardiology: 10.6M, Neurology: 5.0M, Orthopedics: 6.7M)
                return 'rgba(245, 101, 101, 0.9)';                     // Lower revenue - Red (Emergency: 6.7M, Pediatrics: 3.2M)
            });
            // Set max value to show clear differences - don't auto-scale
            maxValue = 12; // Fixed max to show relative differences clearly
            formatter = (value) => '$' + value.toFixed(1) + 'M';
            unit = 'M';
            break;
        case 'occupancy':
            // Convert to percentage and ensure accurate values
            data = departments.map(d => {
                const occupancy = (d.current_occupancy || 0) * 100;
                return Math.round(occupancy * 10) / 10; // Round to 1 decimal place
            });
            label = 'Occupancy Rate (%)';
            color = departments.map((d, i) => {
                const occupancy = data[i];
                if (occupancy >= 90) return 'rgba(239, 68, 68, 0.9)';   // Very high occupancy - Red (Emergency: 92%)
                if (occupancy >= 80) return 'rgba(139, 92, 246, 0.9)';  // High occupancy - Purple (Cardiology: 85%, Oncology: 82%)
                if (occupancy >= 70) return 'rgba(66, 153, 225, 0.9)';  // Medium occupancy - Blue (Surgery: 78%, Orthopedics: 72%)
                return 'rgba(34, 197, 94, 0.9)';                        // Low occupancy - Green (Neurology: 65%, Pediatrics: 58%)
            });
            // Set max value to 100% for occupancy
            maxValue = 100;
            formatter = (value) => value.toFixed(1) + '%';
            unit = '%';
            break;
        default:
            data = departments.map(d => d.patient_satisfaction || 0);
            label = 'Patient Satisfaction Score';
            color = 'rgba(72, 187, 120, 0.9)';
            maxValue = 5;
            formatter = (value) => value.toFixed(1) + '/5';
            unit = '/5';
    }
    
    // Debug log to verify data accuracy
    console.log(`📈 Chart data for ${metric}:`, data);
    console.log('🔧 Revenue values should be: Surgery~11.1, Cardiology~10.6, Emergency~6.7');
    console.log('🔧 Occupancy values should be: Emergency~92, Cardiology~85, Surgery~78');
    console.log('🎯 maxValue set to:', maxValue);
    
    destroyChart('departmentChart');
    chartInstances.departmentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: departments.map(d => d.department_name),
            datasets: [{
                label: label,
                data: data,
                backgroundColor: color,
                borderColor: Array.isArray(color) ? color.map(c => c.replace('0.9', '1')) : color.replace('0.9', '1'),
                borderWidth: 3,
                borderRadius: 12,
                borderSkipped: false,
                hoverBackgroundColor: Array.isArray(color) ? color.map(c => c.replace('0.9', '0.95')) : color.replace('0.9', '0.95'),
                hoverBorderWidth: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            },
            plugins: {
                legend: { 
                    display: true,
                    position: 'top',
                    labels: {
                        font: { size: 16, weight: '700', family: 'Inter' },
                        color: '#1a202c',
                        padding: 25,
                        usePointStyle: true,
                        pointStyle: 'rect',
                        boxWidth: 12,
                        boxHeight: 12
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 32, 44, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#e2e8f0',
                    borderColor: 'rgba(66, 153, 225, 0.8)',
                    borderWidth: 2,
                    cornerRadius: 12,
                    titleFont: { size: 16, weight: '700', family: 'Inter' },
                    bodyFont: { size: 14, family: 'Inter' },
                    padding: 16,
                    displayColors: false,
                    callbacks: {
                        title: function(context) {
                            return context[0].label + ' Department';
                        },
                        label: function(context) {
                            const dept = departments[context.dataIndex];
                            const baseInfo = [`${context.dataset.label}: ${formatter(context.parsed.y)}`];
                            
                            // Add contextual information based on metric
                            if (metric === 'revenue') {
                                const totalRevenue = dept.total_patients * dept.average_cost;
                                baseInfo.push(`Total Patients: ${dept.total_patients.toLocaleString()}`);
                                baseInfo.push(`Avg Cost per Patient: $${dept.average_cost.toLocaleString()}`);
                                baseInfo.push(`Annual Revenue: $${totalRevenue.toLocaleString()}`);
                            } else if (metric === 'occupancy') {
                                baseInfo.push(`Current Capacity: ${(dept.current_occupancy * 100).toFixed(1)}%`);
                                baseInfo.push(`Utilization Level: ${dept.current_occupancy >= 0.9 ? 'Very High' : dept.current_occupancy >= 0.8 ? 'High' : dept.current_occupancy >= 0.7 ? 'Medium' : 'Low'}`);
                            } else {
                                baseInfo.push(`Total Patients: ${dept.total_patients.toLocaleString()}`);
                                baseInfo.push(`Avg Cost: $${dept.average_cost.toLocaleString()}`);
                            }
                            
                            return baseInfo;
                        }
                    }
                }
            },
            scales: {
                y: { 
                    beginAtZero: true, 
                    max: maxValue,
                    grid: {
                        color: 'rgba(203, 213, 224, 0.3)',
                        lineWidth: 1,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#4a5568',
                        font: { size: 13, weight: '600', family: 'Inter' },
                        padding: 12,
                        callback: function(value) {
                            return formatter(value);
                        },
                        // Ensure proper step size for different metrics
                        stepSize: metric === 'revenue' ? 2 : metric === 'occupancy' ? 10 : 0.5
                    },
                    title: {
                        display: true,
                        text: label,
                        color: '#2d3748',
                        font: { size: 14, weight: '700', family: 'Inter' },
                        padding: 20
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#4a5568',
                        font: { size: 12, weight: '600', family: 'Inter' },
                        maxRotation: 0,
                        padding: 8
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

function createTrendsChart(selectedYear = 2024) {
    const ctx = document.getElementById('trendsChart');
    if (!ctx) return;
    
    // All 12 months for better visualization
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    // Multi-year data with realistic healthcare patterns
    const yearData = {
        2024: {
            satisfaction: [4.1, 4.2, 4.0, 4.3, 4.4, 4.5, 4.3, 4.4, 4.6, 4.5, 4.7, 4.6],
            revenue: [8.2, 7.8, 8.5, 9.1, 9.8, 10.2, 9.9, 10.5, 11.2, 10.8, 11.5, 12.1],
            volume: [2100, 1950, 2200, 2350, 2500, 2650, 2550, 2700, 2850, 2750, 2900, 3050]
        },
        2023: {
            satisfaction: [3.9, 4.0, 3.8, 4.1, 4.2, 4.3, 4.1, 4.2, 4.4, 4.3, 4.5, 4.4],
            revenue: [7.8, 7.4, 8.0, 8.6, 9.2, 9.6, 9.3, 9.9, 10.5, 10.2, 10.8, 11.4],
            volume: [1950, 1800, 2050, 2200, 2350, 2500, 2400, 2550, 2700, 2600, 2750, 2900]
        },
        2022: {
            satisfaction: [3.7, 3.8, 3.6, 3.9, 4.0, 4.1, 3.9, 4.0, 4.2, 4.1, 4.3, 4.2],
            revenue: [7.2, 6.8, 7.4, 8.0, 8.6, 9.0, 8.7, 9.3, 9.9, 9.6, 10.2, 10.8],
            volume: [1800, 1650, 1900, 2050, 2200, 2350, 2250, 2400, 2550, 2450, 2600, 2750]
        }
    };
    
    const currentData = yearData[selectedYear];
    
    destroyChart('trendsChart');
    chartInstances.trendsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'Patient Satisfaction',
                data: currentData.satisfaction,
                borderColor: 'rgba(34, 197, 94, 1)',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                borderWidth: 4,
                pointBackgroundColor: 'rgba(34, 197, 94, 1)',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 3,
                pointRadius: 8,
                pointHoverRadius: 10,
                yAxisID: 'y',
                tension: 0.4,
                fill: true
            }, {
                label: 'Revenue ($M)',
                data: currentData.revenue,
                borderColor: 'rgba(59, 130, 246, 1)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 4,
                pointBackgroundColor: 'rgba(59, 130, 246, 1)',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 3,
                pointRadius: 8,
                pointHoverRadius: 10,
                yAxisID: 'y1',
                tension: 0.4,
                fill: true
            }, {
                label: 'Patient Volume',
                data: currentData.volume,
                borderColor: 'rgba(139, 92, 246, 1)',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                borderWidth: 4,
                pointBackgroundColor: 'rgba(139, 92, 246, 1)',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 3,
                pointRadius: 8,
                pointHoverRadius: 10,
                yAxisID: 'y2',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1200,
                easing: 'easeOutQuart'
            },
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: { size: 15, weight: '700', family: 'Inter' },
                        color: '#1a202c',
                        padding: 25,
                        usePointStyle: true,
                        pointStyle: 'circle',
                        boxWidth: 15,
                        boxHeight: 15
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 32, 44, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#e2e8f0',
                    borderColor: 'rgba(59, 130, 246, 0.8)',
                    borderWidth: 2,
                    cornerRadius: 12,
                    titleFont: { size: 16, weight: '700', family: 'Inter' },
                    bodyFont: { size: 14, family: 'Inter' },
                    padding: 16,
                    displayColors: true,
                    usePointStyle: true,
                    callbacks: {
                        title: function(context) {
                            return `${context[0].label} ${selectedYear} Performance`;
                        },
                        label: function(context) {
                            let value = context.parsed.y;
                            if (context.dataset.label === 'Patient Satisfaction') {
                                return `${context.dataset.label}: ${value.toFixed(1)}/5.0 ⭐`;
                            } else if (context.dataset.label === 'Revenue ($M)') {
                                return `${context.dataset.label}: $${value.toFixed(1)}M 💰`;
                            } else {
                                return `${context.dataset.label}: ${value.toLocaleString()} patients 👥`;
                            }
                        },
                        afterBody: function(context) {
                            const monthIndex = context[0].dataIndex;
                            if (monthIndex === 11) { // December
                                return ['', '🎉 Year-end performance summary!'];
                            }
                            return [];
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#4a5568',
                        font: { size: 13, weight: '600', family: 'Inter' },
                        padding: 8
                    }
                },
                y: { 
                    type: 'linear', 
                    display: true, 
                    position: 'left',
                    min: 3.5,
                    max: 5.0,
                    grid: {
                        color: 'rgba(34, 197, 94, 0.2)',
                        lineWidth: 2
                    },
                    ticks: {
                        color: 'rgba(34, 197, 94, 1)',
                        font: { size: 12, weight: '700', family: 'Inter' },
                        padding: 8,
                        callback: function(value) {
                            return value.toFixed(1) + '/5';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Patient Satisfaction ⭐',
                        color: 'rgba(34, 197, 94, 1)',
                        font: { size: 13, weight: '700', family: 'Inter' },
                        padding: 10
                    }
                },
                y1: { 
                    type: 'linear', 
                    display: true, 
                    position: 'right',
                    min: 6,
                    max: 14,
                    grid: {
                        drawOnChartArea: false,
                    },
                    ticks: {
                        color: 'rgba(59, 130, 246, 1)',
                        font: { size: 12, weight: '700', family: 'Inter' },
                        padding: 8,
                        callback: function(value) {
                            return '$' + value.toFixed(1) + 'M';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Revenue 💰',
                        color: 'rgba(59, 130, 246, 1)',
                        font: { size: 13, weight: '700', family: 'Inter' },
                        padding: 10
                    }
                },
                y2: { 
                    type: 'linear', 
                    display: false, 
                    position: 'right',
                    min: 1500,
                    max: 3200
                }
            },
            elements: {
                point: {
                    hoverBackgroundColor: '#ffffff',
                    hoverBorderWidth: 4
                }
            }
        }
    });
}

/**
 * Update department chart based on selected metric
 */
function updateDepartmentChart() {
    console.log('Updating department chart...');
    createDepartmentChart(currentTrendsYear);
}

/**
 * Utility functions
 */
function calculateAverage(data, field) {
    if (!data.length) return 0;
    const sum = data.reduce((acc, item) => acc + (parseFloat(item[field]) || 0), 0);
    return sum / data.length;
}

function updateElement(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
}

function formatCurrency(amount) {
    if (amount >= 1000000000) {
        // Billions
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 1,
            maximumFractionDigits: 1
        }).format(amount / 1000000000) + 'B';
    } else if (amount >= 1000000) {
        // Millions - More compact formatting
        const millions = amount / 1000000;
        if (millions >= 100) {
            return `$${Math.round(millions)}M`;
        } else {
            return `$${millions.toFixed(1)}M`;
        }
    } else if (amount >= 1000) {
        // Thousands - More compact formatting
        const thousands = amount / 1000;
        if (thousands >= 100) {
            return `$${Math.round(thousands)}K`;
        } else {
            return `$${thousands.toFixed(0)}K`;
        }
    } else {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }
}

function destroyChart(chartId) {
    if (chartInstances[chartId]) {
        try {
            chartInstances[chartId].destroy();
        } catch (error) {
            console.warn(`Error destroying chart ${chartId}:`, error);
        }
        delete chartInstances[chartId];
    }
}

// Performance optimization: Destroy all charts when switching dashboards
function destroyAllCharts() {
    Object.keys(chartInstances).forEach(chartId => {
        destroyChart(chartId);
    });
}

// Additional chart functions would continue here...
// (Abbreviated due to length constraints)

/**
 * Create Enhanced Quality Indicators Chart
 */
function createQualityChart(selectedYear = 2024) {
    const ctx = document.getElementById('qualityChart');
    if (!ctx) return;
    
    // Use year-specific quality metrics
    const yearData = healthcareDataByYear[selectedYear] || healthcareDataByYear[2024];
    const qualityMetrics = yearData.qualityMetrics;
    
    destroyChart('qualityChart');
    chartInstances.qualityChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: [
                'Patient Safety',
                'Clinical Excellence', 
                'Patient Experience',
                'Efficiency',
                'Patient Outcomes',
                'Innovation'
            ],
            datasets: [{
                label: `${selectedYear} Performance Score`,
                data: [
                    qualityMetrics.patientSafety,
                    qualityMetrics.clinicalExcellence,
                    qualityMetrics.patientExperience,
                    qualityMetrics.efficiency,
                    qualityMetrics.outcomes,
                    qualityMetrics.innovation
                ],
                backgroundColor: 'rgba(34, 197, 94, 0.2)',
                borderColor: 'rgba(34, 197, 94, 1)',
                borderWidth: 4,
                pointBackgroundColor: 'rgba(34, 197, 94, 1)',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 3,
                pointRadius: 8,
                pointHoverRadius: 10,
                pointHoverBackgroundColor: 'rgba(34, 197, 94, 1)',
                pointHoverBorderColor: '#ffffff',
                pointHoverBorderWidth: 4
            }, {
                label: 'Industry Benchmark',
                data: [85, 83, 80, 82, 84, 78], // Industry standard benchmarks
                backgroundColor: 'rgba(156, 163, 175, 0.1)',
                borderColor: 'rgba(156, 163, 175, 1)',
                borderWidth: 2,
                borderDash: [5, 5],
                pointBackgroundColor: 'rgba(156, 163, 175, 1)',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1500,
                easing: 'easeOutQuart'
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: { size: 14, weight: '700', family: 'Inter' },
                        color: '#1a202c',
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle',
                        boxWidth: 12
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 32, 44, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#e2e8f0',
                    borderColor: 'rgba(34, 197, 94, 0.8)',
                    borderWidth: 2,
                    cornerRadius: 12,
                    titleFont: { size: 15, weight: '700', family: 'Inter' },
                    bodyFont: { size: 13, family: 'Inter' },
                    padding: 16,
                    displayColors: true,
                    usePointStyle: true,
                    callbacks: {
                        title: function(context) {
                            return context[0].label + ' Performance';
                        },
                        label: function(context) {
                            const score = context.parsed.r;
                            let performance = 'Excellent';
                            if (score < 70) performance = 'Needs Improvement';
                            else if (score < 85) performance = 'Good';
                            else if (score < 95) performance = 'Very Good';
                            
                            return [
                                `${context.dataset.label}: ${score.toFixed(1)}/100`,
                                `Performance Level: ${performance} 📈`
                            ];
                        },
                        afterBody: function(context) {
                            const score = context[0].parsed.r;
                            if (score >= 90) {
                                return ['', '✨ Outstanding performance!'];
                            } else if (score >= 85) {
                                return ['', '👍 Strong performance'];
                            }
                            return [];
                        }
                    }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    min: 0,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        color: '#6b7280',
                        font: { size: 11, weight: '600', family: 'Inter' },
                        backdropColor: 'rgba(255, 255, 255, 0.8)',
                        backdropPadding: 4,
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    grid: {
                        color: 'rgba(203, 213, 224, 0.4)',
                        lineWidth: 2
                    },
                    angleLines: {
                        color: 'rgba(203, 213, 224, 0.3)',
                        lineWidth: 1
                    },
                    pointLabels: {
                        color: '#374151',
                        font: { size: 12, weight: '600', family: 'Inter' },
                        padding: 15
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'point'
            }
        }
    });
}

/**
 * Create Hospital Comparison Chart
 */
function createHospitalChart() {
    const ctx = document.getElementById('hospitalChart');
    if (!ctx) return;
    
    // Calculate average satisfaction by hospital from physician data
    const hospitalData = dashboardData.physicians.reduce((acc, physician) => {
        const hospital = physician.hospital;
        if (!acc[hospital]) {
            acc[hospital] = { satisfaction: [], count: 0 };
        }
        acc[hospital].satisfaction.push(physician.patient_satisfaction || 0);
        acc[hospital].count++;
        return acc;
    }, {});
    
    const hospitalAvgs = Object.keys(hospitalData).map(hospital => {
        const satisfactionArray = hospitalData[hospital].satisfaction;
        const avgSatisfaction = satisfactionArray.reduce((a, b) => a + b, 0) / satisfactionArray.length;
        return {
            name: hospital.replace(' Hospital', '').replace(' Medical Center', ' MC'),
            satisfaction: avgSatisfaction,
            physicianCount: hospitalData[hospital].count
        };
    }).sort((a, b) => b.satisfaction - a.satisfaction);
    
    destroyChart('hospitalChart');
    chartInstances.hospitalChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: hospitalAvgs.map(h => h.name),
            datasets: [{
                data: hospitalAvgs.map(h => h.satisfaction),
                backgroundColor: [
                    'rgba(72, 187, 120, 0.8)',
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(159, 122, 234, 0.8)',
                    'rgba(66, 153, 225, 0.8)',
                    'rgba(245, 101, 101, 0.8)',
                    'rgba(129, 140, 248, 0.8)',
                    'rgba(52, 211, 153, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const hospital = hospitalAvgs[context.dataIndex];
                            return `${context.label}: ${hospital.satisfaction.toFixed(1)}/5.0 (${hospital.physicianCount} doctors)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create Revenue by Department Chart
 */
function createRevenueByDeptChart() {
    const ctx = document.getElementById('revenueByDeptChart');
    if (!ctx) return;
    
    // Use calculated financial data with enhanced visual design
    const departments = dashboardData.financialCalculated?.departments || [
        { department_name: 'Surgery', total_patients: 890, average_cost: 12500 },
        { department_name: 'Cardiology', total_patients: 1250, average_cost: 8500 },
        { department_name: 'Oncology', total_patients: 380, average_cost: 15800 },
        { department_name: 'Orthopedics', total_patients: 680, average_cost: 9800 },
        { department_name: 'Emergency', total_patients: 2100, average_cost: 3200 },
        { department_name: 'Neurology', total_patients: 450, average_cost: 11200 },
        { department_name: 'Pediatrics', total_patients: 720, average_cost: 4500 }
    ];
    
    // Calculate revenue and sort by revenue for better visualization
    const revenueData = departments.map(dept => {
        const revenue = (dept.total_patients * dept.average_cost) / 1000000; // Convert to millions
        return {
            name: dept.department_name,
            revenue: revenue,
            patients: dept.total_patients,
            avgCost: dept.average_cost,
            revenuePerPatient: dept.average_cost
        };
    }).sort((a, b) => b.revenue - a.revenue); // Sort by revenue descending
    
    // Create sophisticated color scheme based on revenue performance
    const colors = revenueData.map(dept => {
        if (dept.revenue > 10) return {
            bg: 'rgba(34, 197, 94, 0.9)',   // High revenue - Green
            border: 'rgba(34, 197, 94, 1)',
            hover: 'rgba(34, 197, 94, 0.95)'
        };
        if (dept.revenue > 6) return {
            bg: 'rgba(59, 130, 246, 0.9)',   // Medium-high revenue - Blue 
            border: 'rgba(59, 130, 246, 1)',
            hover: 'rgba(59, 130, 246, 0.95)'
        };
        if (dept.revenue > 4) return {
            bg: 'rgba(139, 92, 246, 0.9)',   // Medium revenue - Purple
            border: 'rgba(139, 92, 246, 1)',
            hover: 'rgba(139, 92, 246, 0.95)'
        };
        return {
            bg: 'rgba(239, 68, 68, 0.9)',     // Lower revenue - Red
            border: 'rgba(239, 68, 68, 1)',
            hover: 'rgba(239, 68, 68, 0.95)'
        };
    });
    
    destroyChart('revenueByDeptChart');
    chartInstances.revenueByDeptChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: revenueData.map(d => d.name),
            datasets: [{
                label: 'Revenue (Millions USD)',
                data: revenueData.map(d => d.revenue),
                backgroundColor: colors.map(c => c.bg),
                borderColor: colors.map(c => c.border),
                hoverBackgroundColor: colors.map(c => c.hover),
                borderWidth: 3,
                borderRadius: 12,
                borderSkipped: false,
                hoverBorderWidth: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            },
            plugins: {
                legend: { 
                    display: false 
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 32, 44, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#e2e8f0',
                    borderColor: 'rgba(59, 130, 246, 0.8)',
                    borderWidth: 2,
                    cornerRadius: 12,
                    titleFont: { size: 16, weight: '700', family: 'Inter' },
                    bodyFont: { size: 14, family: 'Inter' },
                    padding: 16,
                    displayColors: false,
                    callbacks: {
                        title: function(context) {
                            return `🏥 ${context[0].label} Department`;
                        },
                        label: function(context) {
                            const dept = revenueData[context.dataIndex];
                            const performance = dept.revenue > 10 ? 'High Performer 📈' : 
                                              dept.revenue > 6 ? 'Strong Performance 👍' :
                                              dept.revenue > 4 ? 'Moderate Performance 📦' : 'Growth Opportunity 🎯';
                            
                            return [
                                `Revenue: $${dept.revenue.toFixed(1)}M 💰`,
                                `Patients Served: ${dept.patients.toLocaleString()} 👥`,
                                `Avg Cost per Patient: $${dept.avgCost.toLocaleString()} 📊`,
                                `Performance: ${performance}`
                            ];
                        },
                        footer: function(context) {
                            const dept = revenueData[context.dataIndex];
                            const marketShare = ((dept.revenue / revenueData.reduce((sum, d) => sum + d.revenue, 0)) * 100).toFixed(1);
                            return `Market Share: ${marketShare}% of total revenue`;
                        }
                    }
                }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(203, 213, 224, 0.3)',
                        lineWidth: 1,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#4a5568',
                        font: { size: 13, weight: '600', family: 'Inter' },
                        padding: 12,
                        callback: function(value) {
                            return '$' + value.toFixed(1) + 'M';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Revenue (Millions USD) 💰',
                        color: '#2d3748',
                        font: { size: 14, weight: '700', family: 'Inter' },
                        padding: 20
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#4a5568',
                        font: { size: 12, weight: '600', family: 'Inter' },
                        maxRotation: 0,
                        padding: 8
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

/**
 * Create Revenue by Insurance Type Chart
 */
function createRevenueByInsuranceChart() {
    const ctx = document.getElementById('revenueByInsuranceChart');
    if (!ctx) return;
    
    // Realistic insurance distribution in healthcare
    const insuranceData = [
        { type: 'Private Insurance', percentage: 45, revenue: 28.5 },
        { type: 'Medicare', percentage: 35, revenue: 22.1 },
        { type: 'Medicaid', percentage: 15, revenue: 9.5 },
        { type: 'Self-Pay', percentage: 3, revenue: 1.9 },
        { type: 'Commercial', percentage: 2, revenue: 1.3 }
    ];
    
    const colors = [
        'rgba(72, 187, 120, 0.9)',
        'rgba(66, 153, 225, 0.9)',
        'rgba(139, 92, 246, 0.9)',
        'rgba(159, 122, 234, 0.9)',
        'rgba(245, 101, 101, 0.9)'
    ];
    
    destroyChart('revenueByInsuranceChart');
    chartInstances.revenueByInsuranceChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: insuranceData.map(d => d.type),
            datasets: [{
                data: insuranceData.map(d => d.revenue),
                backgroundColor: colors,
                borderColor: '#ffffff',
                borderWidth: 3,
                hoverOffset: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: { size: 13, weight: '600' },
                        color: '#2d3748',
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(45, 55, 72, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: 'rgba(102, 126, 234, 0.8)',
                    borderWidth: 2,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const data = insuranceData[context.dataIndex];
                            return [
                                `Revenue: $${data.revenue}M`,
                                `Percentage: ${data.percentage}%`
                            ];
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create Profitability Chart
 */
function createProfitabilityChart() {
    const ctx = document.getElementById('profitabilityChart');
    if (!ctx) return;
    
    // Department profitability margins (realistic healthcare data)
    const profitData = [
        { department: 'Surgery', margin: 22.5, revenue: 11.1 },
        { department: 'Cardiology', margin: 18.3, revenue: 10.6 },
        { department: 'Oncology', margin: 15.8, revenue: 6.0 },
        { department: 'Orthopedics', margin: 14.2, revenue: 6.7 },
        { department: 'Neurology', margin: 12.7, revenue: 5.0 },
        { department: 'Pediatrics', margin: 8.9, revenue: 3.2 },
        { department: 'Emergency', margin: 6.1, revenue: 6.7 }
    ].sort((a, b) => b.margin - a.margin);
    
    destroyChart('profitabilityChart');
    chartInstances.profitabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: profitData.map(d => d.department),
            datasets: [{
                label: 'Profit Margin (%)',
                data: profitData.map(d => d.margin),
                backgroundColor: profitData.map(d => {
                    if (d.margin > 15) return 'rgba(72, 187, 120, 0.9)';
                    if (d.margin > 10) return 'rgba(66, 153, 225, 0.9)';
                    return 'rgba(139, 92, 246, 0.9)';
                }),
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(45, 55, 72, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    callbacks: {
                        label: function(context) {
                            const dept = profitData[context.dataIndex];
                            return [
                                `Profit Margin: ${dept.margin}%`,
                                `Revenue: $${dept.revenue}M`
                            ];
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 25,
                    grid: {
                        color: 'rgba(45, 55, 72, 0.1)'
                    },
                    ticks: {
                        color: '#4a5568',
                        font: { size: 12, weight: '500' },
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Profit Margin (%)',
                        color: '#2d3748',
                        font: { size: 13, weight: '600' }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#4a5568',
                        font: { size: 11, weight: '500' },
                        maxRotation: 45
                    }
                }
            }
        }
    });
}

/**
 * Create Cost Breakdown Chart
 */
function createCostBreakdownChart() {
    const ctx = document.getElementById('costBreakdownChart');
    if (!ctx) return;
    
    // Hospital cost breakdown (typical healthcare percentages)
    const costData = [
        { category: 'Personnel', amount: 35.2, color: 'rgba(72, 187, 120, 0.9)' },
        { category: 'Medical Supplies', amount: 18.5, color: 'rgba(66, 153, 225, 0.9)' },
        { category: 'Pharmaceuticals', amount: 15.3, color: 'rgba(139, 92, 246, 0.9)' },
        { category: 'Equipment', amount: 12.8, color: 'rgba(159, 122, 234, 0.9)' },
        { category: 'Facility Costs', amount: 8.9, color: 'rgba(245, 101, 101, 0.9)' },
        { category: 'Administrative', amount: 6.1, color: 'rgba(129, 140, 248, 0.9)' },
        { category: 'Other', amount: 3.2, color: 'rgba(52, 211, 153, 0.9)' }
    ];
    
    destroyChart('costBreakdownChart');
    chartInstances.costBreakdownChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: costData.map(d => d.category),
            datasets: [{
                data: costData.map(d => d.amount),
                backgroundColor: costData.map(d => d.color),
                borderColor: '#ffffff',
                borderWidth: 3,
                hoverOffset: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 12, weight: '600' },
                        color: '#2d3748',
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(45, 55, 72, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = costData.reduce((sum, item) => sum + item.amount, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${context.label}: $${value}M (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Parse CSV text to JSON
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
            row[header] = !isNaN(value) && value !== '' ? parseFloat(value) : value;
        });
        return row;
    });
}

/**
 * Parse CSV line handling quotes
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
 * Create Revenue by Insurance Type Chart
 */
function createRevenueByInsuranceChart() {
    const ctx = document.getElementById('revenueByInsuranceChart');
    if (!ctx) return;
    
    const insuranceRevenue = dashboardData.financial.reduce((acc, item) => {
        const insurance = item.insurance_type;
        acc[insurance] = (acc[insurance] || 0) + (item.total_revenue || 0);
        return acc;
    }, {});
    
    destroyChart('revenueByInsuranceChart');
    chartInstances.revenueByInsuranceChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(insuranceRevenue),
            datasets: [{
                data: Object.values(insuranceRevenue),
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(72, 187, 120, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(159, 122, 234, 0.8)',
                    'rgba(245, 101, 101, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

/**
 * Create Profitability Chart
 */
function createProfitabilityChart() {
    const ctx = document.getElementById('profitabilityChart');
    if (!ctx) return;
    
    const deptProfitability = dashboardData.departments.map(dept => ({
        name: dept.department_name,
        revenue: (dept.total_patients || 0) * 5000,
        costs: (dept.total_patients || 0) * 3500,
        margin: ((dept.total_patients || 0) * 1500) / ((dept.total_patients || 0) * 5000) * 100
    }));
    
    destroyChart('profitabilityChart');
    chartInstances.profitabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: deptProfitability.map(d => d.name),
            datasets: [
                {
                    label: 'Revenue',
                    data: deptProfitability.map(d => d.revenue),
                    backgroundColor: 'rgba(72, 187, 120, 0.8)'
                },
                {
                    label: 'Costs',
                    data: deptProfitability.map(d => d.costs),
                    backgroundColor: 'rgba(245, 101, 101, 0.8)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

/**
 * Create Cost Breakdown Chart
 */
function createCostBreakdownChart() {
    const ctx = document.getElementById('costBreakdownChart');
    if (!ctx) return;
    
    const costData = {
        'Staff Costs': 45,
        'Medical Supplies': 20,
        'Equipment': 15,
        'Facilities': 12,
        'Administration': 8
    };
    
    destroyChart('costBreakdownChart');
    chartInstances.costBreakdownChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(costData),
            datasets: [{
                data: Object.values(costData),
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(72, 187, 120, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(159, 122, 234, 0.8)',
                    'rgba(66, 153, 225, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right' }
            }
        }
    });
}

/**
 * Create Demographics Chart
 */
function createDemographicsChart() {
    const ctx = document.getElementById('demographicsChart');
    if (!ctx) return;
    
    const ageGroups = dashboardData.demographics.reduce((acc, item) => {
        const age = item.age_group;
        acc[age] = (acc[age] || 0) + (item.patient_count || 0);
        return acc;
    }, {});
    
    destroyChart('demographicsChart');
    chartInstances.demographicsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(ageGroups),
            datasets: [{
                label: 'Patient Count',
                data: Object.values(ageGroups),
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

/**
 * Create Insurance Distribution Chart
 */
function createInsuranceDistChart() {
    const ctx = document.getElementById('insuranceDistChart');
    if (!ctx) return;
    
    const insuranceDist = dashboardData.demographics.reduce((acc, item) => {
        const insurance = item.insurance_type;
        acc[insurance] = (acc[insurance] || 0) + (item.patient_count || 0);
        return acc;
    }, {});
    
    destroyChart('insuranceDistChart');
    chartInstances.insuranceDistChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(insuranceDist),
            datasets: [{
                data: Object.values(insuranceDist),
                backgroundColor: [
                    'rgba(72, 187, 120, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(66, 153, 225, 0.8)',
                    'rgba(159, 122, 234, 0.8)',
                    'rgba(245, 101, 101, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

/**
 * Create Length of Stay Pattern Chart
 */
function createLOSPatternChart() {
    const ctx = document.getElementById('losPatternChart');
    if (!ctx) return;
    
    const losData = dashboardData.departments.map(dept => ({
        name: dept.department_name,
        avgLOS: dept.average_length_stay || 0,
        readmissionRate: dept.readmission_rate || 0
    }));
    
    destroyChart('losPatternChart');
    chartInstances.losPatternChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'LOS vs Readmission Rate',
                data: losData.map(d => ({ x: d.avgLOS, y: d.readmissionRate })),
                backgroundColor: 'rgba(102, 126, 234, 0.6)',
                borderColor: 'rgba(102, 126, 234, 1)',
                pointRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Average Length of Stay (days)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Readmission Rate (%)'
                    }
                }
            }
        }
    });
}

/**
 * Create Risk Assessment Chart
 */
function createRiskAssessmentChart() {
    const ctx = document.getElementById('riskAssessmentChart');
    if (!ctx) return;
    
    const riskCategories = {
        'Low Risk': 65,
        'Medium Risk': 25,
        'High Risk': 10
    };
    
    destroyChart('riskAssessmentChart');
    chartInstances.riskAssessmentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(riskCategories),
            datasets: [{
                data: Object.values(riskCategories),
                backgroundColor: [
                    'rgba(72, 187, 120, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(245, 101, 101, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

/**
 * Create Top Physicians Chart
 */
function createTopPhysiciansChart(selectedYear = 2024, selectedSpecialty = 'all') {
    const ctx = document.getElementById('topPhysiciansChart');
    if (!ctx) return;
    
    // Use year-specific physician data
    const yearData = healthcareDataByYear[selectedYear] || healthcareDataByYear[2024];
    let physicians = yearData.physicians;
    
    // Filter by specialty if not 'all'
    if (selectedSpecialty && selectedSpecialty !== 'all') {
        physicians = physicians.filter(p => p.specialty === selectedSpecialty);
    }
    
    const topPhysicians = physicians
        .sort((a, b) => (b.patient_satisfaction || 0) - (a.patient_satisfaction || 0))
        .slice(0, 5) // Top 5 physicians
        .map(p => ({
            // Use first name + last initial for compact display
            name: `${p.first_name} ${p.last_name.charAt(0)}.`,
            fullName: `Dr. ${p.first_name} ${p.last_name}`,
            satisfaction: p.patient_satisfaction || 0,
            specialty: p.specialty || 'General'
        }));
    
    // Helper function to get specialty-specific colors
    function getSpecialtyColor(specialty) {
        const colors = {
            'Cardiology': 'rgba(239, 68, 68, 0.8)',    // Red - heart
            'Surgery': 'rgba(59, 130, 246, 0.8)',      // Blue - precision
            'Emergency': 'rgba(245, 158, 11, 0.8)',    // Orange - urgency
            'Pediatrics': 'rgba(16, 185, 129, 0.8)',   // Green - growth
            'Oncology': 'rgba(139, 92, 246, 0.8)',     // Purple - specialty
            'Orthopedics': 'rgba(99, 102, 241, 0.8)',  // Indigo - structure
            'Neurology': 'rgba(236, 72, 153, 0.8)'     // Pink - brain
        };
        return colors[specialty] || 'rgba(72, 187, 120, 0.8)';
    }
    
    destroyChart('topPhysiciansChart');
    chartInstances.topPhysiciansChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topPhysicians.map(p => p.name),
            datasets: [{
                label: `${selectedYear} Patient Satisfaction${selectedSpecialty !== 'all' ? ` (${selectedSpecialty})` : ''}`,
                data: topPhysicians.map(p => p.satisfaction),
                backgroundColor: selectedSpecialty !== 'all' ? 
                    getSpecialtyColor(selectedSpecialty) : 
                    topPhysicians.map(p => getSpecialtyColor(p.specialty)),
                borderColor: selectedSpecialty !== 'all' ? 
                    getSpecialtyColor(selectedSpecialty).replace('0.8', '1') : 
                    topPhysicians.map(p => getSpecialtyColor(p.specialty).replace('0.8', '1')),
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            },
            plugins: {
                legend: { 
                    display: true,
                    position: 'top',
                    labels: {
                        font: { size: 14, weight: '700', family: 'Inter' },
                        color: '#1a202c',
                        padding: 15
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 32, 44, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#e2e8f0',
                    borderColor: 'rgba(72, 187, 120, 0.8)',
                    borderWidth: 2,
                    cornerRadius: 12,
                    titleFont: { size: 15, weight: '700', family: 'Inter' },
                    bodyFont: { size: 13, family: 'Inter' },
                    padding: 16,
                    callbacks: {
                        title: function(context) {
                            const index = context[0].dataIndex;
                            const physician = topPhysicians[index];
                            return `${physician.fullName} (${physician.specialty})`;
                        },
                        label: function(context) {
                            const score = context.parsed.x;
                            let performance = 'Excellent';
                            if (score < 3.5) performance = 'Needs Improvement';
                            else if (score < 4.0) performance = 'Good';
                            else if (score < 4.5) performance = 'Very Good';
                            
                            return [
                                `${selectedYear} Satisfaction: ${score.toFixed(1)}/5.0`,
                                `Performance: ${performance} ⭐`
                            ];
                        },
                        afterBody: function(context) {
                            if (selectedSpecialty !== 'all') {
                                return [`Specialty Focus: ${selectedSpecialty}`];
                            }
                            return [];
                        }
                    }
                }
            },
            scales: {
                x: { 
                    beginAtZero: true, 
                    max: 5,
                    grid: {
                        color: 'rgba(203, 213, 224, 0.4)'
                    },
                    ticks: {
                        color: '#6b7280',
                        font: { size: 12, weight: '600', family: 'Inter' },
                        callback: function(value) {
                            return value.toFixed(1);
                        }
                    },
                    title: {
                        display: true,
                        text: 'Patient Satisfaction Score',
                        color: '#374151',
                        font: { size: 13, weight: '700', family: 'Inter' },
                        padding: 15
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#374151',
                        font: { size: 12, weight: '600', family: 'Inter' },
                        maxRotation: 0, // Keep labels horizontal
                        minRotation: 0
                    },
                    title: {
                        display: true,
                        text: selectedSpecialty !== 'all' ? `${selectedSpecialty} Specialists` : 'All Specialties',
                        color: '#374151',
                        font: { size: 13, weight: '700', family: 'Inter' },
                        padding: 15
                    }
                }
            },
            layout: {
                padding: {
                    left: 10,
                    right: 20,
                    top: 10,
                    bottom: 10
                }
            }
        }
    });
}

/**
 * Create Specialty Performance Chart
 */
function createSpecialtyPerformanceChart() {
    const ctx = document.getElementById('specialtyPerformanceChart');
    if (!ctx) return;
    
    const specialtyPerf = dashboardData.physicians.reduce((acc, physician) => {
        const specialty = physician.specialty;
        if (!acc[specialty]) {
            acc[specialty] = { satisfaction: [], successRate: [] };
        }
        acc[specialty].satisfaction.push(physician.patient_satisfaction || 0);
        acc[specialty].successRate.push(physician.success_rate || 0);
        return acc;
    }, {});
    
    const chartData = Object.keys(specialtyPerf).map(specialty => {
        const satisfaction = specialtyPerf[specialty].satisfaction;
        const successRate = specialtyPerf[specialty].successRate;
        return {
            specialty,
            avgSatisfaction: satisfaction.reduce((a, b) => a + b, 0) / satisfaction.length,
            avgSuccessRate: successRate.reduce((a, b) => a + b, 0) / successRate.length
        };
    });
    
    destroyChart('specialtyPerformanceChart');
    chartInstances.specialtyPerformanceChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: chartData.map(d => d.specialty),
            datasets: [
                {
                    label: 'Patient Satisfaction',
                    data: chartData.map(d => d.avgSatisfaction),
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    pointBackgroundColor: 'rgba(102, 126, 234, 1)'
                },
                {
                    label: 'Success Rate',
                    data: chartData.map(d => d.avgSuccessRate / 20), // Scale to match satisfaction
                    backgroundColor: 'rgba(72, 187, 120, 0.2)',
                    borderColor: 'rgba(72, 187, 120, 1)',
                    pointBackgroundColor: 'rgba(72, 187, 120, 1)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: { beginAtZero: true, max: 5 }
            }
        }
    });
}

/**
 * Create Workload Chart
 */
function createWorkloadChart() {
    const ctx = document.getElementById('workloadChart');
    if (!ctx) return;
    
    const workloadData = dashboardData.physicians.map(p => ({
        name: `${p.first_name} ${p.last_name}`,
        patients: p.total_patients || 0,
        waitTime: p.average_wait_time || 0
    })).sort((a, b) => b.patients - a.patients).slice(0, 15);
    
    destroyChart('workloadChart');
    chartInstances.workloadChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Patient Load vs Wait Time',
                data: workloadData.map(d => ({ x: d.patients, y: d.waitTime })),
                backgroundColor: 'rgba(139, 92, 246, 0.6)',
                borderColor: 'rgba(139, 92, 246, 1)',
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Total Patients'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Average Wait Time (minutes)'
                    }
                }
            }
        }
    });
}

/**
 * Create Physician Quality Chart
 */
function createPhysicianQualityChart() {
    const ctx = document.getElementById('physicianQualityChart');
    if (!ctx) return;
    
    const qualityMetrics = dashboardData.physicians.map(p => ({
        satisfaction: p.patient_satisfaction || 0,
        successRate: p.success_rate || 0,
        complicationRate: 10 - (p.complication_rate || 0) // Invert for better visualization
    }));
    
    const avgMetrics = {
        satisfaction: qualityMetrics.reduce((sum, m) => sum + m.satisfaction, 0) / qualityMetrics.length,
        successRate: qualityMetrics.reduce((sum, m) => sum + m.successRate, 0) / qualityMetrics.length,
        complicationRate: qualityMetrics.reduce((sum, m) => sum + m.complicationRate, 0) / qualityMetrics.length
    };
    
    destroyChart('physicianQualityChart');
    chartInstances.physicianQualityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Patient Satisfaction', 'Success Rate', 'Low Complication Rate'],
            datasets: [{
                label: 'Quality Metrics',
                data: [avgMetrics.satisfaction, avgMetrics.successRate / 20, avgMetrics.complicationRate],
                backgroundColor: [
                    'rgba(72, 187, 120, 0.8)',
                    'rgba(66, 153, 225, 0.8)',
                    'rgba(159, 122, 234, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true, max: 5 }
            }
        }
    });
}

/**
 * Update Department Chart based on selected metric
 */
function updateDepartmentChart() {
    const metric = document.getElementById('performanceMetric')?.value || 'satisfaction';
    const ctx = document.getElementById('departmentChart');
    if (!ctx) return;
    
    let data, label, color;
    
    switch(metric) {
        case 'satisfaction':
            data = dashboardData.departments.map(d => d.patient_satisfaction || 0);
            label = 'Patient Satisfaction';
            color = 'rgba(102, 126, 234, 0.8)';
            break;
        case 'revenue':
            data = dashboardData.departments.map(d => (d.total_patients || 0) * 5000);
            label = 'Revenue ($)';
            color = 'rgba(72, 187, 120, 0.8)';
            break;
        case 'occupancy':
            data = dashboardData.departments.map(d => (d.current_occupancy || 0) * 100);
            label = 'Occupancy Rate (%)';
            color = 'rgba(66, 153, 225, 0.8)';
            break;
    }
    
    if (chartInstances.departmentChart) {
        chartInstances.departmentChart.data.datasets[0].data = data;
        chartInstances.departmentChart.data.datasets[0].label = label;
        chartInstances.departmentChart.data.datasets[0].backgroundColor = color;
        chartInstances.departmentChart.data.datasets[0].borderColor = color;
        chartInstances.departmentChart.update();
    }
}

/**
 * Utility Functions
 */
function showLoadingState() {
    // Add loading indicators to dashboard sections
    const sections = document.querySelectorAll('.dashboard-section');
    sections.forEach(section => {
        const loading = document.createElement('div');
        loading.className = 'loading-overlay';
        loading.innerHTML = '<div class="loading-spinner"></div><p>Loading dashboard data...</p>';
        loading.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.9);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        `;
        section.style.position = 'relative';
        section.appendChild(loading);
    });
}

function hideLoadingState() {
    // Remove loading indicators
    const loadingOverlays = document.querySelectorAll('.loading-overlay');
    loadingOverlays.forEach(overlay => overlay.remove());
}

function showError(message) {
    // Create error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'dashboard-error';
    errorDiv.innerHTML = `
        <div class="error-content">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Dashboard Error</h3>
            <p>${message}</p>
            <button onclick="location.reload()" class="btn btn-primary">Retry</button>
        </div>
    `;
    errorDiv.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
        color: white;
        text-align: center;
    `;
    
    document.body.appendChild(errorDiv);
}

/**
 * Change Trends Chart Year
 * Updates all dashboard charts and KPIs to show data for the selected year
 */
function changeTrendsYear(year) {
    // Update current year
    currentTrendsYear = year;
    
    // Update active tab styling
    document.querySelectorAll('.year-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`[data-year="${year}"]`).classList.add('active');
    
    // Get year-specific data
    const yearData = healthcareDataByYear[year] || healthcareDataByYear[2024];
    
    // Update KPIs with year-specific data
    updateKPIsForYear(year, yearData);
    
    // Update all synchronized charts with smooth transitions
    setTimeout(() => {
        const selectedSpecialty = document.getElementById('physicianSpecialty')?.value || 'all';
        createTrendsChart(year);
        createDepartmentChart(year);
        createQualityChart(year);
        createTopPhysiciansChart(year, selectedSpecialty);
    }, 100);
    
    console.log(`📅 Dashboard synchronized to ${year} data`);
}

/**
 * Update KPIs for selected year
 */
function updateKPIsForYear(year, yearData) {
    const departments = yearData.departments;
    
    // Calculate year-specific KPIs
    const totalRevenue = departments.reduce((sum, dept) => sum + (dept.total_patients * dept.average_cost), 0);
    const avgSatisfaction = departments.reduce((sum, dept) => sum + dept.patient_satisfaction, 0) / departments.length;
    const avgOccupancy = departments.reduce((sum, dept) => sum + dept.current_occupancy, 0) / departments.length;
    const qualityScore = departments.reduce((sum, dept) => sum + dept.quality_score, 0) / departments.length;
    
    // Update KPI displays with year-specific data
    updateElement('totalRevenue', formatCurrency(totalRevenue));
    updateElement('avgSatisfaction', avgSatisfaction.toFixed(1) + '/5.0');
    updateElement('occupancyRate', (avgOccupancy * 100).toFixed(1) + '%');
    updateElement('qualityScore', qualityScore.toFixed(1) + '/100');
}

// Make function globally available
window.changeTrendsYear = changeTrendsYear;

/**
 * Update Top Physicians Chart based on specialty selection
 */
function updateTopPhysiciansChart() {
    const selectedSpecialty = document.getElementById('physicianSpecialty')?.value || 'all';
    createTopPhysiciansChart(currentTrendsYear, selectedSpecialty);
    console.log(`👩‍⚕️ Physicians chart updated for ${selectedSpecialty} specialty in ${currentTrendsYear}`);
}

// Make function globally available
window.updateTopPhysiciansChart = updateTopPhysiciansChart;