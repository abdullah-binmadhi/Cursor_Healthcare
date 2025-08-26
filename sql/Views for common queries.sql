DROP VIEW IF EXISTS patient_summary;
DROP VIEW IF EXISTS department_performance;
DROP VIEW IF EXISTS monthly_metrics;
DROP VIEW IF EXISTS high_risk_patients;
DROP VIEW IF EXISTS current_census;
DROP VIEW IF EXISTS top_diagnoses;
DROP VIEW IF EXISTS physician_performance;
DROP VIEW IF EXISTS financial_summary;

-- 1. PATIENT SUMMARY VIEW (SQLite Compatible)
CREATE VIEW patient_summary AS
SELECT 
    p.patient_id,
    p.first_name || ' ' || p.last_name AS full_name,
    p.date_of_birth,
    CASE 
        WHEN p.date_of_birth IS NOT NULL THEN 
            CAST((julianday('now') - julianday(p.date_of_birth)) / 365.25 AS INTEGER)
        ELSE NULL 
    END AS current_age,
    p.gender,
    p.insurance_type,
    COUNT(a.admission_id) AS total_admissions,
    MAX(a.admission_date) AS last_admission_date,
    ROUND(AVG(a.length_of_stay), 2) AS avg_length_of_stay,
    COALESCE(SUM(fd.net_revenue), 0) AS total_net_revenue
FROM patients p
LEFT JOIN admissions a ON p.patient_id = a.patient_id
LEFT JOIN financial_data fd ON a.admission_id = fd.admission_id
GROUP BY p.patient_id, p.first_name, p.last_name, p.date_of_birth, p.gender, p.insurance_type;

-- 2. DEPARTMENT PERFORMANCE VIEW (SQLite Compatible)
CREATE VIEW department_performance AS
SELECT 
    a.department,
    COUNT(*) AS total_admissions,
    ROUND(AVG(a.length_of_stay), 2) AS avg_length_of_stay,
    ROUND(AVG(qm.patient_satisfaction_score), 2) AS avg_satisfaction,
    ROUND(AVG(fd.net_revenue), 2) AS avg_revenue_per_case,
    COUNT(r.readmission_id) AS total_readmissions,
    ROUND(
        CASE 
            WHEN COUNT(*) > 0 THEN (CAST(COUNT(r.readmission_id) AS REAL) * 100.0 / COUNT(*))
            ELSE 0 
        END, 2
    ) AS readmission_rate
FROM admissions a
LEFT JOIN quality_metrics qm ON a.admission_id = qm.admission_id
LEFT JOIN financial_data fd ON a.admission_id = fd.admission_id
LEFT JOIN readmissions r ON a.admission_id = r.original_admission_id
WHERE a.discharge_date IS NOT NULL
GROUP BY a.department
ORDER BY total_admissions DESC;

-- 3. MONTHLY METRICS VIEW (SQLite Compatible)
CREATE VIEW monthly_metrics AS
SELECT 
    date(a.admission_date, 'start of month') AS month_year,
    COUNT(*) AS total_admissions,
    COUNT(a.discharge_date) AS total_discharges,
    ROUND(AVG(a.length_of_stay), 2) AS avg_length_of_stay,
    ROUND(AVG(qm.patient_satisfaction_score), 2) AS avg_satisfaction,
    COALESCE(SUM(fd.net_revenue), 0) AS total_revenue,
    ROUND(AVG(fd.net_revenue), 2) AS avg_revenue_per_case,
    COUNT(r.readmission_id) AS total_readmissions
FROM admissions a
LEFT JOIN quality_metrics qm ON a.admission_id = qm.admission_id
LEFT JOIN financial_data fd ON a.admission_id = fd.admission_id
LEFT JOIN readmissions r ON a.admission_id = r.original_admission_id
GROUP BY date(a.admission_date, 'start of month')
ORDER BY month_year;

-- 4. HIGH-RISK PATIENTS VIEW (SQLite Compatible)
CREATE VIEW high_risk_patients AS
SELECT 
    p.patient_id,
    p.first_name || ' ' || p.last_name AS full_name,
    CASE 
        WHEN p.date_of_birth IS NOT NULL THEN 
            CAST((julianday('now') - julianday(p.date_of_birth)) / 365.25 AS INTEGER)
        ELSE NULL 
    END AS age,
    COUNT(a.admission_id) AS admission_count,
    COUNT(r.readmission_id) AS readmission_count,
    ROUND(AVG(qm.mortality_risk_score), 3) AS avg_mortality_risk,
    MAX(a.admission_date) AS last_admission
FROM patients p
JOIN admissions a ON p.patient_id = a.patient_id
LEFT JOIN readmissions r ON a.admission_id = r.original_admission_id
LEFT JOIN quality_metrics qm ON a.admission_id = qm.admission_id
GROUP BY p.patient_id, p.first_name, p.last_name, p.date_of_birth
HAVING COUNT(a.admission_id) > 3 
    OR COUNT(r.readmission_id) > 0 
    OR AVG(qm.mortality_risk_score) > 0.1
ORDER BY readmission_count DESC, avg_mortality_risk DESC;

-- 5. CURRENT CENSUS VIEW (SQLite Compatible)
CREATE VIEW current_census AS
SELECT
    department,
    COUNT(*) as current_patients,
    ROUND(AVG(julianday('now') - julianday(admission_date)), 1) as avg_days_admitted,
    ROUND(AVG(length_of_stay), 1) as avg_expected_los
FROM admissions 
WHERE discharge_date IS NULL
GROUP BY department
ORDER BY current_patients DESC;

-- 6. TOP DIAGNOSES VIEW (SQLite Compatible)
CREATE VIEW top_diagnoses AS
SELECT 
    d.diagnosis_description,
    COUNT(*) as case_count,
    ROUND(AVG(a.length_of_stay), 1) as avg_los,
    ROUND(AVG(fd.net_revenue), 2) as avg_revenue,
    ROUND(SUM(fd.net_revenue), 2) as total_revenue
FROM diagnoses d
JOIN admissions a ON d.admission_id = a.admission_id
JOIN financial_data fd ON a.admission_id = fd.admission_id
WHERE d.diagnosis_type = 'Primary'
GROUP BY d.diagnosis_description
ORDER BY case_count DESC;

-- 7. PHYSICIAN PERFORMANCE VIEW (SQLite Compatible)
CREATE VIEW physician_performance AS
SELECT 
    attending_physician as physician_name,
    COUNT(*) as total_cases,
    ROUND(AVG(length_of_stay), 1) as avg_los,
    ROUND(AVG(fd.net_revenue), 2) as avg_revenue,
    COUNT(CASE WHEN discharge_date IS NULL THEN 1 END) as current_patients,
    ROUND(AVG(qm.patient_satisfaction_score), 2) as avg_satisfaction
FROM admissions a
LEFT JOIN financial_data fd ON a.admission_id = fd.admission_id
LEFT JOIN quality_metrics qm ON a.admission_id = qm.admission_id
GROUP BY attending_physician
HAVING COUNT(*) >= 3
ORDER BY total_cases DESC;

-- 8. FINANCIAL SUMMARY VIEW (SQLite Compatible)
CREATE VIEW financial_summary AS
SELECT 
    strftime('%Y-%m', a.admission_date) as month_year,
    COUNT(*) as total_admissions,
    ROUND(SUM(fd.total_charges), 2) as total_charges,
    ROUND(SUM(fd.insurance_payment), 2) as insurance_payments,
    ROUND(SUM(fd.patient_payment), 2) as patient_payments,
    ROUND(SUM(fd.net_revenue), 2) as net_revenue,
    ROUND(AVG(fd.net_revenue), 2) as avg_revenue_per_case,
    ROUND(SUM(fd.adjustment_amount), 2) as total_adjustments
FROM admissions a
JOIN financial_data fd ON a.admission_id = fd.admission_id
GROUP BY strftime('%Y-%m', a.admission_date)
ORDER BY month_year DESC;