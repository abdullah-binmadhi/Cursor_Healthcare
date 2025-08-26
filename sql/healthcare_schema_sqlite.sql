-- ====================
-- HEALTHCARE DATABASE SCHEMA (SQLite Compatible)
-- ====================

-- 1. PATIENTS TABLE (Master patient information)
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    gender TEXT CHECK (gender IN ('M', 'F', 'Other', 'Unknown')),
    race TEXT,
    ethnicity TEXT,
    zip_code TEXT,
    insurance_type TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. ADMISSIONS TABLE (Each hospital stay)
CREATE TABLE IF NOT EXISTS admissions (
    admission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    admission_date DATE NOT NULL,
    discharge_date DATE,
    admission_type TEXT CHECK (admission_type IN ('Emergency', 'Elective', 'Urgent', 'Transfer')),
    discharge_status TEXT CHECK (discharge_status IN ('Home', 'Transfer', 'AMA', 'Expired', 'SNF')),
    length_of_stay INTEGER,
    department TEXT,
    attending_physician TEXT,
    room_number TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. DIAGNOSES TABLE (Medical conditions)
CREATE TABLE IF NOT EXISTS diagnoses (
    diagnosis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_id INTEGER,
    diagnosis_code TEXT, -- ICD-10 codes
    diagnosis_description TEXT,
    diagnosis_type TEXT CHECK (diagnosis_type IN ('Primary', 'Secondary', 'Comorbidity')),
    severity_level INTEGER CHECK (severity_level BETWEEN 1 AND 5),
    chronic_condition BOOLEAN DEFAULT FALSE
);

-- 4. PROCEDURES TABLE (Treatments and procedures)
CREATE TABLE IF NOT EXISTS procedures (
    procedure_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_id INTEGER,
    procedure_code TEXT, -- CPT codes
    procedure_description TEXT,
    procedure_date DATE,
    performing_physician TEXT,
    procedure_duration INTEGER, -- minutes
    procedure_cost REAL
);

-- 5. FINANCIAL DATA TABLE (Billing and costs)
CREATE TABLE IF NOT EXISTS financial_data (
    financial_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_id INTEGER,
    total_charges REAL,
    insurance_payment REAL,
    patient_payment REAL,
    adjustment_amount REAL,
    write_off_amount REAL,
    net_revenue REAL,
    billing_date DATE,
    payment_date DATE
);

-- 6. READMISSIONS TABLE (Track return visits)
CREATE TABLE IF NOT EXISTS readmissions (
    readmission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_admission_id INTEGER,
    readmission_admission_id INTEGER,
    days_between_admissions INTEGER,
    same_diagnosis BOOLEAN,
    preventable_flag BOOLEAN,
    readmission_type TEXT CHECK (readmission_type IN ('Planned', 'Unplanned', 'Related', 'Unrelated'))
);

-- 7. QUALITY METRICS TABLE (Patient outcomes and satisfaction)
CREATE TABLE IF NOT EXISTS quality_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_id INTEGER,
    patient_satisfaction_score REAL CHECK (patient_satisfaction_score BETWEEN 1.0 AND 5.0),
    pain_management_score REAL,
    communication_score REAL,
    cleanliness_score REAL,
    mortality_risk_score REAL,
    complication_occurred BOOLEAN DEFAULT FALSE,
    infection_acquired BOOLEAN DEFAULT FALSE,
    survey_completion_date DATE
);

-- 8. VITAL SIGNS TABLE (Clinical measurements)
CREATE TABLE IF NOT EXISTS vital_signs (
    vital_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admission_id INTEGER,
    measurement_date TIMESTAMP,
    systolic_bp INTEGER,
    diastolic_bp INTEGER,
    heart_rate INTEGER,
    temperature REAL,
    respiratory_rate INTEGER,
    oxygen_saturation INTEGER,
    weight_kg REAL,
    height_cm INTEGER,
    bmi REAL
);
