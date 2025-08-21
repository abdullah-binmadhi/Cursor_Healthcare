-- ====================
-- ESSENTIAL HEALTHCARE ANALYTICS QUERIES
-- ====================
-- Collection of essential SQL queries for healthcare analytics
-- Compatible with SQLite database

-- ====================
-- 1. CURRENT PATIENT CENSUS BY DEPARTMENT
-- ====================
SELECT
    department,
    COUNT(*) as current_patients,
    ROUND(AVG(julianday('now') - julianday(admission_date)), 1) as avg_days_admitted
FROM admissions 
WHERE discharge_date IS NULL
GROUP BY department
ORDER BY current_patients DESC;

-- ====================
-- 2. MONTHLY ADMISSION TRENDS (LAST 12 MONTHS)
-- ====================
SELECT 
    strftime('%Y-%m', admission_date) as month,
    COUNT(*) as admissions,
    ROUND(AVG(length_of_stay), 1) as avg_los
FROM admissions 
WHERE admission_date >= date('now', '-12 months')
GROUP BY strftime('%Y-%m', admission_date)
ORDER BY month;

-- ====================
-- 3. TOP DIAGNOSES BY VOLUME
-- ====================
SELECT 
    d.diagnosis_description,
    COUNT(*) as case_count,
    ROUND(AVG(a.length_of_stay), 1) as avg_los,
    ROUND(AVG(fd.net_revenue), 2) as avg_revenue
FROM diagnoses d
JOIN admissions a ON d.admission_id = a.admission_id
JOIN financial_data fd ON a.admission_id = fd.admission_id
WHERE d.diagnosis_type = 'Primary'
GROUP BY d.diagnosis_description
ORDER BY case_count DESC
LIMIT 20;

-- ====================
-- 4. READMISSION ANALYSIS (LAST 30 DAYS)
-- ====================
SELECT 
    a.department,
    COUNT(DISTINCT a.admission_id) as total_discharges,
    COUNT(r.readmission_id) as readmissions,
    ROUND(
        CASE 
            WHEN COUNT(DISTINCT a.admission_id) > 0 THEN
                (CAST(COUNT(r.readmission_id) AS REAL) * 100.0 / COUNT(DISTINCT a.admission_id))
            ELSE 0 
        END, 2
    ) as readmission_rate
FROM admissions a
LEFT JOIN readmissions r ON a.admission_id = r.original_admission_id
WHERE a.discharge_date >= date('now', '-30 days')
  AND a.discharge_date IS NOT NULL
GROUP BY a.department
ORDER BY readmission_rate DESC;

-- ====================
-- 5. PATIENT SATISFACTION BY DEPARTMENT (LAST 90 DAYS)
-- ====================
SELECT 
    a.department,
    COUNT(qm.metric_id) as surveys_completed,
    ROUND(AVG(qm.patient_satisfaction_score), 2) as avg_satisfaction,
    ROUND(AVG(qm.communication_score), 2) as avg_communication,
    ROUND(AVG(qm.pain_management_score), 2) as avg_pain_mgmt
FROM admissions a
JOIN quality_metrics qm ON a.admission_id = qm.admission_id
WHERE qm.survey_completion_date >= date('now', '-90 days')
GROUP BY a.department
ORDER BY avg_satisfaction DESC;

-- ====================
-- 6. DAILY ADMISSION VOLUME TREND (LAST 30 DAYS)
-- ====================
SELECT 
    date(admission_date) as admission_day,
    COUNT(*) as daily_admissions,
    strftime('%w', admission_date) as day_of_week  -- 0=Sunday, 1=Monday, etc.
FROM admissions 
WHERE admission_date >= date('now', '-30 days')
GROUP BY date(admission_date)
ORDER BY admission_day DESC;

-- ====================
-- 7. LENGTH OF STAY DISTRIBUTION BY DEPARTMENT
-- ====================
SELECT 
    department,
    COUNT(*) as total_cases,
    MIN(length_of_stay) as min_los,
    ROUND(AVG(length_of_stay), 1) as avg_los,
    MAX(length_of_stay) as max_los,
    -- Quartiles approximation
    COUNT(CASE WHEN length_of_stay <= 2 THEN 1 END) as short_stay_count,
    COUNT(CASE WHEN length_of_stay > 7 THEN 1 END) as long_stay_count
FROM admissions 
WHERE discharge_date IS NOT NULL
GROUP BY department
ORDER BY avg_los DESC;

-- ====================
-- 8. REVENUE ANALYSIS BY INSURANCE TYPE
-- ====================
SELECT 
    p.insurance_type,
    COUNT(*) as case_count,
    ROUND(AVG(fd.net_revenue), 2) as avg_revenue,
    ROUND(SUM(fd.net_revenue), 2) as total_revenue,
    ROUND(AVG(a.length_of_stay), 1) as avg_los
FROM patients p
JOIN admissions a ON p.patient_id = a.patient_id
JOIN financial_data fd ON a.admission_id = fd.admission_id
WHERE a.discharge_date IS NOT NULL
GROUP BY p.insurance_type
ORDER BY total_revenue DESC;

-- ====================
-- 9. HIGH-VOLUME PHYSICIANS
-- ====================
SELECT 
    attending_physician as physician_name,
    COUNT(*) as total_cases,
    ROUND(AVG(length_of_stay), 1) as avg_los,
    COUNT(CASE WHEN discharge_date IS NULL THEN 1 END) as current_patients
FROM admissions 
WHERE admission_date >= date('now', '-90 days')
GROUP BY attending_physician
HAVING COUNT(*) >= 5   -- Only physicians with 5+ cases
ORDER BY total_cases DESC;

-- ====================
-- 10. WEEKEND VS WEEKDAY ADMISSIONS
-- ====================
SELECT 
    CASE 
        WHEN strftime('%w', admission_date) IN ('0', '6') THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    COUNT(*) as admission_count,
    ROUND(AVG(length_of_stay), 1) as avg_los,
    ROUND(COUNT(*) * 100.0 / (
        SELECT COUNT(*) FROM admissions 
        WHERE admission_date >= date('now', '-90 days')
    ), 1) as percentage
FROM admissions 
WHERE admission_date >= date('now', '-90 days')
GROUP BY day_type;

-- ====================
-- ADDITIONAL USEFUL ANALYTICS QUERIES
-- ====================

-- ====================
-- 11. EMERGENCY VS ELECTIVE ADMISSIONS BY MONTH
-- ====================
SELECT 
    strftime('%Y-%m', admission_date) as month,
    admission_type,
    COUNT(*) as admission_count,
    ROUND(AVG(length_of_stay), 1) as avg_los,
    ROUND(AVG(fd.net_revenue), 2) as avg_revenue
FROM admissions a
JOIN financial_data fd ON a.admission_id = fd.admission_id
WHERE admission_date >= date('now', '-12 months')
GROUP BY strftime('%Y-%m', admission_date), admission_type
ORDER BY month DESC, admission_type;

-- ====================
-- 12. PATIENT AGE DISTRIBUTION BY DIAGNOSIS
-- ====================
SELECT 
    d.diagnosis_description,
    ROUND(AVG(CAST(strftime('%Y', 'now') AS INTEGER) - CAST(strftime('%Y', p.date_of_birth) AS INTEGER)), 1) as avg_age,
    COUNT(*) as patient_count,
    MIN(CAST(strftime('%Y', 'now') AS INTEGER) - CAST(strftime('%Y', p.date_of_birth) AS INTEGER)) as min_age,
    MAX(CAST(strftime('%Y', 'now') AS INTEGER) - CAST(strftime('%Y', p.date_of_birth) AS INTEGER)) as max_age
FROM diagnoses d
JOIN admissions a ON d.admission_id = a.admission_id
JOIN patients p ON a.patient_id = p.patient_id
WHERE d.diagnosis_type = 'Primary'
  AND p.date_of_birth IS NOT NULL
GROUP BY d.diagnosis_description
ORDER BY patient_count DESC;

-- ====================
-- 13. ROOM UTILIZATION ANALYSIS
-- ====================
SELECT 
    room_number,
    COUNT(*) as total_admissions,
    ROUND(AVG(length_of_stay), 1) as avg_los,
    COUNT(CASE WHEN discharge_date IS NULL THEN 1 END) as currently_occupied,
    ROUND(SUM(fd.net_revenue), 2) as total_revenue
FROM admissions a
JOIN financial_data fd ON a.admission_id = fd.admission_id
WHERE room_number IS NOT NULL AND room_number != ''
GROUP BY room_number
ORDER BY total_admissions DESC
LIMIT 20;

-- ====================
-- 14. PROCEDURE COST ANALYSIS
-- ====================
SELECT 
    procedure_description,
    COUNT(*) as procedure_count,
    ROUND(AVG(procedure_cost), 2) as avg_cost,
    ROUND(SUM(procedure_cost), 2) as total_cost,
    ROUND(AVG(procedure_duration), 1) as avg_duration_minutes
FROM procedures
WHERE procedure_cost > 0
GROUP BY procedure_description
ORDER BY total_cost DESC
LIMIT 15;

-- ====================
-- 15. FINANCIAL PERFORMANCE SUMMARY
-- ====================
SELECT 
    strftime('%Y-%m', a.admission_date) as month,
    COUNT(*) as total_admissions,
    ROUND(SUM(fd.total_charges), 2) as total_charges,
    ROUND(SUM(fd.insurance_payment), 2) as insurance_payments,
    ROUND(SUM(fd.patient_payment), 2) as patient_payments,
    ROUND(SUM(fd.net_revenue), 2) as net_revenue,
    ROUND(AVG(fd.net_revenue), 2) as avg_revenue_per_case
FROM admissions a
JOIN financial_data fd ON a.admission_id = fd.admission_id
WHERE a.admission_date >= date('now', '-12 months')
GROUP BY strftime('%Y-%m', a.admission_date)
ORDER BY month DESC;
