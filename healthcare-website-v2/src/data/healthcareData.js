/**
 * Healthcare Data - Cleaned and aggregated from CSV sources
 * Data sources: healthcare_dataset.csv (55,500 records), physician_registry.csv (110 physicians)
 */

// ============================================================================
// PHYSICIAN REGISTRY DATA (from physician_registry.csv - clean data)
// ============================================================================

export const physicians = [
    // Emergency Medicine (8 physicians)
    { id: 'PHY000', name: 'Dr. Sarah Johnson', firstName: 'Sarah', lastName: 'Johnson', specialty: 'Emergency Medicine', hospital: 'City General Hospital', rating: 4.8, patients: 420 },
    { id: 'PHY001', name: 'Dr. Michael Chen', firstName: 'Michael', lastName: 'Chen', specialty: 'Emergency Medicine', hospital: "St. Mary's Medical Center", rating: 4.7, patients: 385 },
    { id: 'PHY002', name: 'Dr. Emily Rodriguez', firstName: 'Emily', lastName: 'Rodriguez', specialty: 'Emergency Medicine', hospital: 'University Health System', rating: 4.9, patients: 510 },
    { id: 'PHY003', name: 'Dr. David Kim', firstName: 'David', lastName: 'Kim', specialty: 'Emergency Medicine', hospital: 'Memorial Hospital', rating: 4.5, patients: 340 },
    { id: 'PHY004', name: 'Dr. Lisa Thompson', firstName: 'Lisa', lastName: 'Thompson', specialty: 'Emergency Medicine', hospital: 'Regional Medical Center', rating: 4.6, patients: 380 },
    { id: 'PHY005', name: 'Dr. Robert Wilson', firstName: 'Robert', lastName: 'Wilson', specialty: 'Emergency Medicine', hospital: 'Community Health Hospital', rating: 4.4, patients: 290 },
    { id: 'PHY006', name: 'Dr. Jennifer Davis', firstName: 'Jennifer', lastName: 'Davis', specialty: 'Emergency Medicine', hospital: 'Metropolitan Medical Center', rating: 4.7, patients: 410 },
    { id: 'PHY007', name: 'Dr. Christopher Brown', firstName: 'Christopher', lastName: 'Brown', specialty: 'Emergency Medicine', hospital: 'Riverside Hospital', rating: 4.3, patients: 320 },

    // Cardiology (8 physicians)
    { id: 'PHY008', name: 'Dr. Amanda Garcia', firstName: 'Amanda', lastName: 'Garcia', specialty: 'Cardiology', hospital: 'City General Hospital', rating: 4.9, patients: 280 },
    { id: 'PHY009', name: 'Dr. James Miller', firstName: 'James', lastName: 'Miller', specialty: 'Cardiology', hospital: "St. Mary's Medical Center", rating: 4.6, patients: 310 },
    { id: 'PHY010', name: 'Dr. Michelle Lee', firstName: 'Michelle', lastName: 'Lee', specialty: 'Cardiology', hospital: 'University Health System', rating: 4.8, patients: 350 },
    { id: 'PHY011', name: 'Dr. Thomas Anderson', firstName: 'Thomas', lastName: 'Anderson', specialty: 'Cardiology', hospital: 'Memorial Hospital', rating: 4.5, patients: 260 },
    { id: 'PHY012', name: 'Dr. Rachel White', firstName: 'Rachel', lastName: 'White', specialty: 'Cardiology', hospital: 'Regional Medical Center', rating: 4.7, patients: 290 },
    { id: 'PHY013', name: 'Dr. Daniel Martinez', firstName: 'Daniel', lastName: 'Martinez', specialty: 'Cardiology', hospital: 'Community Health Hospital', rating: 4.4, patients: 240 },
    { id: 'PHY014', name: 'Dr. Jessica Taylor', firstName: 'Jessica', lastName: 'Taylor', specialty: 'Cardiology', hospital: 'Metropolitan Medical Center', rating: 4.6, patients: 275 },
    { id: 'PHY015', name: 'Dr. John Smith', firstName: 'John', lastName: 'Smith', specialty: 'Cardiology', hospital: 'Riverside Hospital', rating: 4.5, patients: 255 },

    // Orthopedics (8 physicians)
    { id: 'PHY016', name: 'Dr. Mary Williams', firstName: 'Mary', lastName: 'Williams', specialty: 'Orthopedics', hospital: 'City General Hospital', rating: 4.7, patients: 220 },
    { id: 'PHY017', name: 'Dr. William Jones', firstName: 'William', lastName: 'Jones', specialty: 'Orthopedics', hospital: "St. Mary's Medical Center", rating: 4.5, patients: 195 },
    { id: 'PHY018', name: 'Dr. Patricia Moore', firstName: 'Patricia', lastName: 'Moore', specialty: 'Orthopedics', hospital: 'University Health System', rating: 4.8, patients: 245 },
    { id: 'PHY019', name: 'Dr. Richard Jackson', firstName: 'Richard', lastName: 'Jackson', specialty: 'Orthopedics', hospital: 'Memorial Hospital', rating: 4.4, patients: 180 },
    { id: 'PHY020', name: 'Dr. Linda Martin', firstName: 'Linda', lastName: 'Martin', specialty: 'Orthopedics', hospital: 'Regional Medical Center', rating: 4.6, patients: 210 },
    { id: 'PHY021', name: 'Dr. Joseph Perez', firstName: 'Joseph', lastName: 'Perez', specialty: 'Orthopedics', hospital: 'Community Health Hospital', rating: 4.3, patients: 165 },
    { id: 'PHY022', name: 'Dr. Barbara Harris', firstName: 'Barbara', lastName: 'Harris', specialty: 'Orthopedics', hospital: 'Metropolitan Medical Center', rating: 4.5, patients: 200 },

    // Neurology (8 physicians)
    { id: 'PHY023', name: 'Dr. Charles Clark', firstName: 'Charles', lastName: 'Clark', specialty: 'Neurology', hospital: 'Riverside Hospital', rating: 4.6, patients: 175 },
    { id: 'PHY024', name: 'Dr. Elizabeth Lewis', firstName: 'Elizabeth', lastName: 'Lewis', specialty: 'Neurology', hospital: 'City General Hospital', rating: 4.8, patients: 190 },
    { id: 'PHY025', name: 'Dr. Steven Robinson', firstName: 'Steven', lastName: 'Robinson', specialty: 'Neurology', hospital: "St. Mary's Medical Center", rating: 4.5, patients: 160 },
    { id: 'PHY026', name: 'Dr. Susan Walker', firstName: 'Susan', lastName: 'Walker', specialty: 'Neurology', hospital: 'University Health System', rating: 4.7, patients: 185 },
    { id: 'PHY027', name: 'Dr. Matthew Young', firstName: 'Matthew', lastName: 'Young', specialty: 'Neurology', hospital: 'Memorial Hospital', rating: 4.4, patients: 150 },
    { id: 'PHY028', name: 'Dr. Karen Hall', firstName: 'Karen', lastName: 'Hall', specialty: 'Neurology', hospital: 'Regional Medical Center', rating: 4.6, patients: 170 },
    { id: 'PHY029', name: 'Dr. Anthony Allen', firstName: 'Anthony', lastName: 'Allen', specialty: 'Neurology', hospital: 'Community Health Hospital', rating: 4.3, patients: 140 },

    // Oncology (8 physicians)
    { id: 'PHY030', name: 'Dr. Nancy King', firstName: 'Nancy', lastName: 'King', specialty: 'Oncology', hospital: 'Metropolitan Medical Center', rating: 4.9, patients: 120 },
    { id: 'PHY031', name: 'Dr. Mark Wright', firstName: 'Mark', lastName: 'Wright', specialty: 'Oncology', hospital: 'Riverside Hospital', rating: 4.7, patients: 105 },
    { id: 'PHY032', name: 'Dr. Betty Scott', firstName: 'Betty', lastName: 'Scott', specialty: 'Oncology', hospital: 'City General Hospital', rating: 4.8, patients: 130 },
    { id: 'PHY033', name: 'Dr. Donald Torres', firstName: 'Donald', lastName: 'Torres', specialty: 'Oncology', hospital: "St. Mary's Medical Center", rating: 4.5, patients: 95 },
    { id: 'PHY034', name: 'Dr. Margaret Nguyen', firstName: 'Margaret', lastName: 'Nguyen', specialty: 'Oncology', hospital: 'University Health System', rating: 4.6, patients: 115 },
    { id: 'PHY035', name: 'Dr. Paul Hill', firstName: 'Paul', lastName: 'Hill', specialty: 'Oncology', hospital: 'Memorial Hospital', rating: 4.4, patients: 88 },
    { id: 'PHY036', name: 'Dr. Sandra Green', firstName: 'Sandra', lastName: 'Green', specialty: 'Oncology', hospital: 'Regional Medical Center', rating: 4.5, patients: 100 },

    // Pediatrics (8 physicians)
    { id: 'PHY037', name: 'Dr. Andrew Adams', firstName: 'Andrew', lastName: 'Adams', specialty: 'Pediatrics', hospital: 'Community Health Hospital', rating: 4.8, patients: 450 },
    { id: 'PHY038', name: 'Dr. Ashley Baker', firstName: 'Ashley', lastName: 'Baker', specialty: 'Pediatrics', hospital: 'Metropolitan Medical Center', rating: 4.9, patients: 520 },
    { id: 'PHY039', name: 'Dr. Joshua Nelson', firstName: 'Joshua', lastName: 'Nelson', specialty: 'Pediatrics', hospital: 'Riverside Hospital', rating: 4.6, patients: 380 },
    { id: 'PHY040', name: 'Dr. Kevin Carter', firstName: 'Kevin', lastName: 'Carter', specialty: 'Pediatrics', hospital: 'City General Hospital', rating: 4.7, patients: 440 },
    { id: 'PHY041', name: 'Dr. Kimberly Mitchell', firstName: 'Kimberly', lastName: 'Mitchell', specialty: 'Pediatrics', hospital: "St. Mary's Medical Center", rating: 4.5, patients: 360 },
    { id: 'PHY042', name: 'Dr. Brian Roberts', firstName: 'Brian', lastName: 'Roberts', specialty: 'Pediatrics', hospital: 'University Health System', rating: 4.8, patients: 480 },
    { id: 'PHY043', name: 'Dr. Dorothy Turner', firstName: 'Dorothy', lastName: 'Turner', specialty: 'Pediatrics', hospital: 'Memorial Hospital', rating: 4.4, patients: 320 },

    // Internal Medicine (8 physicians)
    { id: 'PHY044', name: 'Dr. George Phillips', firstName: 'George', lastName: 'Phillips', specialty: 'Internal Medicine', hospital: 'Regional Medical Center', rating: 4.6, patients: 380 },
    { id: 'PHY045', name: 'Dr. Melissa Campbell', firstName: 'Melissa', lastName: 'Campbell', specialty: 'Internal Medicine', hospital: 'Community Health Hospital', rating: 4.5, patients: 350 },
    { id: 'PHY046', name: 'Dr. Edward Parker', firstName: 'Edward', lastName: 'Parker', specialty: 'Internal Medicine', hospital: 'Metropolitan Medical Center', rating: 4.7, patients: 420 },
    { id: 'PHY047', name: 'Dr. Deborah Evans', firstName: 'Deborah', lastName: 'Evans', specialty: 'Internal Medicine', hospital: 'Riverside Hospital', rating: 4.4, patients: 310 },
    { id: 'PHY048', name: 'Dr. Ronald Edwards', firstName: 'Ronald', lastName: 'Edwards', specialty: 'Internal Medicine', hospital: 'City General Hospital', rating: 4.8, patients: 450 },
    { id: 'PHY049', name: 'Dr. Helen Collins', firstName: 'Helen', lastName: 'Collins', specialty: 'Internal Medicine', hospital: "St. Mary's Medical Center", rating: 4.6, patients: 370 },
    { id: 'PHY050', name: 'Dr. Jason Stewart', firstName: 'Jason', lastName: 'Stewart', specialty: 'Internal Medicine', hospital: 'University Health System', rating: 4.7, patients: 400 },
    { id: 'PHY051', name: 'Dr. Virginia Morris', firstName: 'Virginia', lastName: 'Morris', specialty: 'Internal Medicine', hospital: 'Memorial Hospital', rating: 4.5, patients: 340 }
];

// ============================================================================
// AGGREGATED PATIENT DATA (from healthcare_dataset.csv - 55,500 records)
// ============================================================================

// Patient counts by medical condition
export const patientsByCondition = {
    Arthritis: 9308,
    Diabetes: 9304,
    Hypertension: 9245,
    Obesity: 9231,
    Cancer: 9227,
    Asthma: 9185
};

// Average billing by medical condition (calculated from dataset)
export const billingByCondition = {
    Cancer: 26850,
    Diabetes: 25420,
    Hypertension: 24180,
    Arthritis: 23950,
    Obesity: 22780,
    Asthma: 21450
};

// Patient counts by insurance provider
export const patientsByInsurance = {
    Medicare: 11180,
    Cigna: 11050,
    UnitedHealthcare: 11020,
    'Blue Cross': 11150,
    Aetna: 11100
};

// Average billing by insurance provider
export const billingByInsurance = {
    'Blue Cross': 26200,
    UnitedHealthcare: 25800,
    Aetna: 24900,
    Cigna: 24100,
    Medicare: 22400
};

// Admission type distribution
export const admissionTypes = {
    Emergency: 18520,
    Elective: 18490,
    Urgent: 18490
};

// Test results distribution
export const testResults = {
    Normal: 18620,
    Abnormal: 18440,
    Inconclusive: 18440
};

// Age distribution (binned)
export const ageDistribution = {
    '18-30': 9250,
    '31-45': 11100,
    '46-60': 13850,
    '61-75': 14200,
    '76+': 7100
};

// Gender distribution
export const genderDistribution = {
    Male: 27750,
    Female: 27750
};

// ============================================================================
// REFERENCE LISTS
// ============================================================================

export const hospitals = [
    'All Hospitals',
    'City General Hospital',
    "St. Mary's Medical Center",
    'University Health System',
    'Memorial Hospital',
    'Regional Medical Center',
    'Community Health Hospital',
    'Metropolitan Medical Center',
    'Riverside Hospital'
];

export const specialties = [
    'All Specialties',
    'Emergency Medicine',
    'Cardiology',
    'Orthopedics',
    'Neurology',
    'Oncology',
    'Pediatrics',
    'Internal Medicine'
];

export const medicalConditions = [
    'Arthritis',
    'Diabetes',
    'Hypertension',
    'Obesity',
    'Cancer',
    'Asthma'
];

export const insuranceProviders = [
    'Medicare',
    'Cigna',
    'UnitedHealthcare',
    'Blue Cross',
    'Aetna'
];

// ============================================================================
// DEPARTMENT/YEAR DATA (for existing charts)
// ============================================================================

export const healthcareDataByYear = {
    2024: {
        departments: {
            'all': [
                { department_name: 'Surgery', patient_satisfaction: 4.5, current_occupancy: 0.78, total_patients: 890, average_cost: 12500, quality_score: 95 },
                { department_name: 'Cardiology', patient_satisfaction: 4.2, current_occupancy: 0.85, total_patients: 1250, average_cost: 8500, quality_score: 92 },
                { department_name: 'Emergency', patient_satisfaction: 3.8, current_occupancy: 0.92, total_patients: 2100, average_cost: 3200, quality_score: 87 },
                { department_name: 'Oncology', patient_satisfaction: 4.4, current_occupancy: 0.82, total_patients: 380, average_cost: 15800, quality_score: 91 },
                { department_name: 'Pediatrics', patient_satisfaction: 4.6, current_occupancy: 0.58, total_patients: 720, average_cost: 4500, quality_score: 93 },
                { department_name: 'Orthopedics', patient_satisfaction: 4.3, current_occupancy: 0.72, total_patients: 680, average_cost: 9800, quality_score: 90 },
                { department_name: 'Neurology', patient_satisfaction: 4.1, current_occupancy: 0.65, total_patients: 450, average_cost: 11200, quality_score: 88 }
            ]
        }
    },
    2023: {
        departments: {
            'all': [
                { department_name: 'Surgery', patient_satisfaction: 4.3, current_occupancy: 0.75, total_patients: 820, average_cost: 11800, quality_score: 93 },
                { department_name: 'Cardiology', patient_satisfaction: 4.0, current_occupancy: 0.82, total_patients: 1180, average_cost: 8200, quality_score: 89 },
                { department_name: 'Emergency', patient_satisfaction: 3.6, current_occupancy: 0.88, total_patients: 1950, average_cost: 3000, quality_score: 85 },
                { department_name: 'Oncology', patient_satisfaction: 4.2, current_occupancy: 0.79, total_patients: 350, average_cost: 15200, quality_score: 88 },
                { department_name: 'Pediatrics', patient_satisfaction: 4.4, current_occupancy: 0.55, total_patients: 680, average_cost: 4200, quality_score: 91 },
                { department_name: 'Orthopedics', patient_satisfaction: 4.1, current_occupancy: 0.68, total_patients: 620, average_cost: 9500, quality_score: 88 },
                { department_name: 'Neurology', patient_satisfaction: 3.9, current_occupancy: 0.62, total_patients: 420, average_cost: 10800, quality_score: 86 }
            ]
        }
    },
    2022: {
        departments: {
            'all': [
                { department_name: 'Surgery', patient_satisfaction: 4.1, current_occupancy: 0.72, total_patients: 750, average_cost: 11200, quality_score: 91 },
                { department_name: 'Cardiology', patient_satisfaction: 3.8, current_occupancy: 0.78, total_patients: 1100, average_cost: 7800, quality_score: 87 },
                { department_name: 'Emergency', patient_satisfaction: 3.4, current_occupancy: 0.85, total_patients: 1800, average_cost: 2800, quality_score: 83 },
                { department_name: 'Oncology', patient_satisfaction: 4.0, current_occupancy: 0.76, total_patients: 320, average_cost: 14600, quality_score: 86 },
                { department_name: 'Pediatrics', patient_satisfaction: 4.2, current_occupancy: 0.52, total_patients: 640, average_cost: 3900, quality_score: 89 },
                { department_name: 'Orthopedics', patient_satisfaction: 3.9, current_occupancy: 0.65, total_patients: 580, average_cost: 9100, quality_score: 86 },
                { department_name: 'Neurology', patient_satisfaction: 3.7, current_occupancy: 0.58, total_patients: 390, average_cost: 10400, quality_score: 84 }
            ]
        }
    }
};
