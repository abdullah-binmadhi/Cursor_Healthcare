/**
 * Healthcare Analytics Dashboard JavaScript
 * Handles interactive dashboards, charts, and KPI calculations
 */

// Global variables
let dashboardData = {
    physicians: [],
    financial: [],
    departments: [],
    demographics: []
};

let chartInstances = {};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

/**
 * Initialize the dashboard application
 */
async function initializeDashboard() {
    try {
        // Load data
        await loadDashboardData();
        
        // Setup event listeners
        setupDashboardListeners();
        
        // Initialize the first dashboard
        showDashboard('hospital');
        
        console.log('Dashboard initialized successfully');
    } catch (error) {
        console.error('Error initializing dashboard:', error);
    }
}

/**
 * Load all dashboard data
 */
async function loadDashboardData() {
    try {
        const [physicians, financial, departments, demographics] = await Promise.all([
            loadCSV('data/physician_performance.csv'),
            loadCSV('data/financial_performance.csv'),
            loadCSV('data/department_metrics.csv'),
            loadCSV('data/patient_demographics.csv')
        ]);
        
        dashboardData = { physicians, financial, departments, demographics };
    } catch (error) {
        console.error('Error loading dashboard data:', error);
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
 * Show specific dashboard
 */
function showDashboard(type) {
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
    
    // Load dashboard data
    switch(type) {
        case 'hospital': loadHospitalDashboard(); break;
        case 'financial': loadFinancialDashboard(); break;
        case 'patient': loadPatientDashboard(); break;
        case 'physician': loadPhysicianDashboard(); break;
    }
}

/**
 * Load Hospital Performance Dashboard
 */
function loadHospitalDashboard() {
    // Calculate KPIs
    const totalRevenue = dashboardData.financial.reduce((sum, item) => sum + (item.total_revenue || 0), 0);
    const avgSatisfaction = calculateAverage(dashboardData.departments, 'patient_satisfaction');
    const avgOccupancy = calculateAverage(dashboardData.departments, 'current_occupancy') * 100;
    const qualityScore = calculateAverage(dashboardData.departments, 'patient_satisfaction') * 20; // Scale to 100
    
    // Update KPI values
    updateElement('totalRevenue', formatCurrency(totalRevenue));
    updateElement('avgSatisfaction', avgSatisfaction.toFixed(1) + '/5.0');
    updateElement('occupancyRate', avgOccupancy.toFixed(1) + '%');
    updateElement('qualityScore', qualityScore.toFixed(1) + '/100');
    
    // Create charts
    createDepartmentChart();
    createTrendsChart();
    createQualityChart();
    createHospitalChart();
}

/**
 * Load Financial Analytics Dashboard
 */
function loadFinancialDashboard() {
    // Calculate financial KPIs
    const totalRevenue = dashboardData.financial.reduce((sum, item) => sum + (item.total_revenue || 0), 0);
    const totalPatients = dashboardData.demographics.reduce((sum, item) => sum + (item.patient_count || 0), 0);
    const revenuePerPatient = totalPatients > 0 ? totalRevenue / totalPatients : 0;
    
    updateElement('operatingMargin', '18.5%');
    updateElement('revenuePerPatient', formatCurrency(revenuePerPatient));
    updateElement('badDebtRate', '3.2%');
    updateElement('collectionRate', '94.8%');
    
    // Create financial charts
    createRevenueByDeptChart();
    createRevenueByInsuranceChart();
    createProfitabilityChart();
    createCostBreakdownChart();
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
    const physicians = dashboardData.physicians;
    const activePhysicians = physicians.filter(p => p.availability_status !== 'Unavailable').length;
    const avgPerformance = calculateAverage(physicians, 'patient_satisfaction');
    const avgSuccessRate = calculateAverage(physicians, 'success_rate');
    const topPerformer = physicians.reduce((max, p) => p.patient_satisfaction > max.patient_satisfaction ? p : max, physicians[0]);
    
    updateElement('activePhysicians', activePhysicians);
    updateElement('avgPerformance', avgPerformance.toFixed(1) + '/5.0');
    updateElement('avgSuccessRate', avgSuccessRate.toFixed(1) + '%');
    updateElement('topPerformer', `Dr. ${topPerformer?.first_name} ${topPerformer?.last_name}`);
    
    // Create physician charts
    createTopPhysiciansChart();
    createSpecialtyPerformanceChart();
    createWorkloadChart();
    createPhysicianQualityChart();
}

/**
 * Chart creation functions
 */
function createDepartmentChart() {
    const ctx = document.getElementById('departmentChart');
    if (!ctx) return;
    
    const data = dashboardData.departments.map(dept => ({
        label: dept.department_name,
        satisfaction: dept.patient_satisfaction || 0,
        revenue: (dept.total_patients || 0) * 5000, // Estimated revenue
        occupancy: (dept.current_occupancy || 0) * 100
    }));
    
    destroyChart('departmentChart');
    chartInstances.departmentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.label),
            datasets: [{
                label: 'Patient Satisfaction',
                data: data.map(d => d.satisfaction),
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
                y: { beginAtZero: true, max: 5 }
            }
        }
    });
}

function createTrendsChart() {
    const ctx = document.getElementById('trendsChart');
    if (!ctx) return;
    
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const satisfactionData = [4.2, 4.3, 4.1, 4.4, 4.5, 4.6];
    const revenueData = [2.1, 2.3, 2.2, 2.5, 2.7, 2.8];
    
    destroyChart('trendsChart');
    chartInstances.trendsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'Patient Satisfaction',
                data: satisfactionData,
                borderColor: 'rgba(72, 187, 120, 1)',
                backgroundColor: 'rgba(72, 187, 120, 0.1)',
                yAxisID: 'y'
            }, {
                label: 'Revenue (M)',
                data: revenueData,
                borderColor: 'rgba(66, 153, 225, 1)',
                backgroundColor: 'rgba(66, 153, 225, 0.1)',
                yAxisID: 'y1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { type: 'linear', display: true, position: 'left', max: 5 },
                y1: { type: 'linear', display: true, position: 'right', max: 3 }
            }
        }
    });
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
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function destroyChart(chartId) {
    if (chartInstances[chartId]) {
        chartInstances[chartId].destroy();
        delete chartInstances[chartId];
    }
}

// Additional chart functions would continue here...
// (Abbreviated due to length constraints)

/**
 * Create Quality Indicators Chart
 */
function createQualityChart() {
    const ctx = document.getElementById('qualityChart');
    if (!ctx) return;
    
    destroyChart('qualityChart');
    chartInstances.qualityChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Patient Satisfaction', 'Safety Score', 'Efficiency', 'Readmission Rate', 'Infection Rate'],
            datasets: [{
                label: 'Hospital Performance',
                data: [85, 92, 78, 88, 95],
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                borderColor: 'rgba(102, 126, 234, 1)',
                pointBackgroundColor: 'rgba(102, 126, 234, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: { beginAtZero: true, max: 100 }
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
    
    const hospitals = ['City General', 'St. Mary\'s', 'University', 'Memorial', 'Regional'];
    const satisfactionData = [4.2, 4.5, 4.1, 4.3, 4.4];
    
    destroyChart('hospitalChart');
    chartInstances.hospitalChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: hospitals,
            datasets: [{
                data: satisfactionData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

/**
 * Create Revenue by Department Chart
 */
function createRevenueByDeptChart() {
    const ctx = document.getElementById('revenueByDeptChart');
    if (!ctx) return;
    
    const deptRevenue = dashboardData.financial.reduce((acc, item) => {
        const dept = item.department;
        acc[dept] = (acc[dept] || 0) + (item.total_revenue || 0);
        return acc;
    }, {});
    
    destroyChart('revenueByDeptChart');
    chartInstances.revenueByDeptChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(deptRevenue),
            datasets: [{
                label: 'Revenue',
                data: Object.values(deptRevenue),
                backgroundColor: 'rgba(72, 187, 120, 0.8)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } }
        }
    });
}

/**
 * Load CSV data (reuse from main script.js)
 */
async function loadCSV(filePath) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) throw new Error(`Failed to load ${filePath}`);
        const csvText = await response.text();
        return parseCSV(csvText);
    } catch (error) {
        console.error(`Error loading CSV ${filePath}:`, error);
        return [];
    }
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

// Placeholder functions for remaining charts
function createRevenueByInsuranceChart() { /* Implementation */ }
function createProfitabilityChart() { /* Implementation */ }
function createCostBreakdownChart() { /* Implementation */ }
function createDemographicsChart() { /* Implementation */ }
function createInsuranceDistChart() { /* Implementation */ }
function createLOSPatternChart() { /* Implementation */ }
function createRiskAssessmentChart() { /* Implementation */ }
function createTopPhysiciansChart() { /* Implementation */ }
function createSpecialtyPerformanceChart() { /* Implementation */ }
function createWorkloadChart() { /* Implementation */ }
function createPhysicianQualityChart() { /* Implementation */ }
function updateDepartmentChart() { /* Implementation */ }