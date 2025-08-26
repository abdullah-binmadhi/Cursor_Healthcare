-- ====================
-- PERFORMANCE INDEXES
-- ====================

-- Primary lookup indexes
CREATE INDEX idx_patients_name ON patients(last_name, first_name);
CREATE INDEX idx_patients_dob ON patients(date_of_birth);
CREATE INDEX idx_admissions_dates ON admissions(admission_date, discharge_date);
CREATE INDEX idx_admissions_patient ON admissions(patient_id);

-- Analytics indexes  
CREATE INDEX idx_diagnoses_code ON diagnoses(diagnosis_code);
CREATE INDEX idx_procedures_code ON procedures(procedure_code);
CREATE INDEX idx_financial_revenue ON financial_data(net_revenue);
CREATE INDEX idx_quality_satisfaction ON quality_metrics(patient_satisfaction_score);

-- Composite indexes for common queries
CREATE INDEX idx_admissions_dept_date ON admissions(department, admission_date);
CREATE INDEX idx_readmissions_days ON readmissions(days_between_admissions);
CREATE INDEX idx_vitals_date ON vital_signs(admission_id, measurement_date);