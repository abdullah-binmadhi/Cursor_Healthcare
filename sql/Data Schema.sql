-- ====================
-- HEALTHCARE DATABASE SCHEMA
-- ====================

-- 1. PATIENTS TABLE (Master patient information)
CREATE TABLE patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(10) CHECK (gender IN ('M', 'F', 'Other', 'Unknown')),
    race VARCHAR(50),
    ethnicity VARCHAR(50),
    zip_code VARCHAR(10),
    insurance_type VARCHAR(50),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. ADMISSIONS TABLE (Each hospital stay)
CREATE TABLE admissions (
    admission_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    admission_date DATE NOT NULL,
    discharge_date DATE,
    admission_type VARCHAR(50) CHECK (admission_type IN ('Emergency', 'Elective', 'Urgent', 'Transfer')),
    discharge_status VARCHAR(50) CHECK (discharge_status IN ('Home', 'Transfer', 'AMA', 'Expired', 'SNF')),
    length_of_stay INTEGER GENERATED ALWAYS AS (discharge_date - admission_date) STORED,
    department VARCHAR(100),
    attending_physician VARCHAR(100),
    room_number VARCHAR(20),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. DIAGNOSES TABLE (Medical conditions)
CREATE TABLE diagnoses (
    diagnosis_id SERIAL PRIMARY KEY,
    admission_id INTEGER REFERENCES admissions(admission_id),
    diagnosis_code VARCHAR(20), -- ICD-10 codes
    diagnosis_description TEXT,
    diagnosis_type VARCHAR(20) CHECK (diagnosis_type IN ('Primary', 'Secondary', 'Comorbidity')),
    severity_level INTEGER CHECK (severity_level BETWEEN 1 AND 5),
    chronic_condition BOOLEAN DEFAULT FALSE
);

-- 4. PROCEDURES TABLE (Treatments and procedures)
CREATE TABLE procedures (
    procedure_id SERIAL PRIMARY KEY,
    admission_id INTEGER REFERENCES admissions(admission_id),
    procedure_code VARCHAR(20), -- CPT codes
    procedure_description TEXT,
    procedure_date DATE,
    performing_physician VARCHAR(100),
    procedure_duration INTEGER, -- minutes
    procedure_cost DECIMAL(10,2)
);

-- 5. FINANCIAL DATA TABLE (Billing and costs)
CREATE TABLE financial_data (
    financial_id SERIAL PRIMARY KEY,
    admission_id INTEGER REFERENCES admissions(admission_id),
    total_charges DECIMAL(12,2),
    insurance_payment DECIMAL(12,2),
    patient_payment DECIMAL(12,2),
    adjustment_amount DECIMAL(12,2),
    write_off_amount DECIMAL(12,2),
    net_revenue DECIMAL(12,2) GENERATED ALWAYS AS (
        COALESCE(insurance_payment,0) + COALESCE(patient_payment,0) - COALESCE(write_off_amount,0)
    ) STORED,
    billing_date DATE,
    payment_date DATE
);

-- 6. READMISSIONS TABLE (Track return visits)
CREATE TABLE readmissions (
    readmission_id SERIAL PRIMARY KEY,
    original_admission_id INTEGER REFERENCES admissions(admission_id),
    readmission_admission_id INTEGER REFERENCES admissions(admission_id),
    days_between_admissions INTEGER,
    same_diagnosis BOOLEAN,
    preventable_flag BOOLEAN,
    readmission_type VARCHAR(50) CHECK (readmission_type IN ('Planned', 'Unplanned', 'Related', 'Unrelated'))
);

-- 7. QUALITY METRICS TABLE (Patient outcomes and satisfaction)
CREATE TABLE quality_metrics (
    metric_id SERIAL PRIMARY KEY,
    admission_id INTEGER REFERENCES admissions(admission_id),
    patient_satisfaction_score DECIMAL(3,2) CHECK (patient_satisfaction_score BETWEEN 1.0 AND 5.0),
    pain_management_score DECIMAL(3,2),
    communication_score DECIMAL(3,2),
    cleanliness_score DECIMAL(3,2),
    mortality_risk_score DECIMAL(5,4),
    complication_occurred BOOLEAN DEFAULT FALSE,
    infection_acquired BOOLEAN DEFAULT FALSE,
    survey_completion_date DATE
);

-- 8. VITAL SIGNS TABLE (Clinical measurements)
CREATE TABLE vital_signs (
    vital_id SERIAL PRIMARY KEY,
    admission_id INTEGER REFERENCES admissions(admission_id),
    measurement_date TIMESTAMP,
    systolic_bp INTEGER,
    diastolic_bp INTEGER,
    heart_rate INTEGER,
    temperature DECIMAL(4,2),
    respiratory_rate INTEGER,
    oxygen_saturation INTEGER,
    weight_kg DECIMAL(5,2),
    height_cm INTEGER,
    bmi DECIMAL(4,2) GENERATED ALWAYS AS (
        CASE WHEN height_cm > 0 THEN weight_kg / POWER(height_cm/100.0, 2) ELSE NULL END
    ) STORED
);