#!/usr/bin/env python3
"""
PostgreSQL Healthcare Analytics Queries
Executes healthcare analytics queries on PostgreSQL database
"""

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text
from datetime import datetime
import sys
import os

def get_postgresql_engine():
    """Create PostgreSQL engine with environment variables"""
    
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'healthcare_analytics')
    
    connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    return create_engine(connection_string)

def run_postgresql_analytics():
    """Run comprehensive healthcare analytics on PostgreSQL"""
    
    try:
        engine = get_postgresql_engine()
        
        print("=" * 80)
        print("POSTGRESQL HEALTHCARE ANALYTICS DASHBOARD")
        print("=" * 80)
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Define PostgreSQL-compatible analytics queries
        analytics_queries = [
            {
                "name": "CURRENT PATIENT CENSUS BY DEPARTMENT",
                "query": """
                    SELECT
                        department,
                        COUNT(*) as current_patients,
                        ROUND(AVG(CURRENT_DATE - admission_date), 1) as avg_days_admitted
                    FROM admissions 
                    WHERE discharge_date IS NULL
                    GROUP BY department
                    ORDER BY current_patients DESC
                """
            },
            {
                "name": "MONTHLY ADMISSION TRENDS (LAST 12 MONTHS)",
                "query": """
                    SELECT 
                        TO_CHAR(admission_date, 'YYYY-MM') as month,
                        COUNT(*) as admissions,
                        ROUND(AVG(length_of_stay), 1) as avg_los
                    FROM admissions 
                    WHERE admission_date >= CURRENT_DATE - INTERVAL '12 months'
                    GROUP BY TO_CHAR(admission_date, 'YYYY-MM')
                    ORDER BY month
                """
            },
            {
                "name": "TOP DIAGNOSES BY VOLUME",
                "query": """
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
                    LIMIT 20
                """
            },
            {
                "name": "READMISSION ANALYSIS (LAST 30 DAYS)",
                "query": """
                    SELECT 
                        a.department,
                        COUNT(DISTINCT a.admission_id) as total_discharges,
                        COUNT(r.readmission_id) as readmissions,
                        ROUND(
                            CASE 
                                WHEN COUNT(DISTINCT a.admission_id) > 0 THEN
                                    (COUNT(r.readmission_id)::DECIMAL * 100.0 / COUNT(DISTINCT a.admission_id))
                                ELSE 0 
                            END, 2
                        ) as readmission_rate
                    FROM admissions a
                    LEFT JOIN readmissions r ON a.admission_id = r.original_admission_id
                    WHERE a.discharge_date >= CURRENT_DATE - INTERVAL '30 days'
                      AND a.discharge_date IS NOT NULL
                    GROUP BY a.department
                    ORDER BY readmission_rate DESC
                """
            },
            {
                "name": "PATIENT SATISFACTION BY DEPARTMENT (LAST 90 DAYS)",
                "query": """
                    SELECT 
                        a.department,
                        COUNT(qm.metric_id) as surveys_completed,
                        ROUND(AVG(qm.patient_satisfaction_score), 2) as avg_satisfaction,
                        ROUND(AVG(qm.communication_score), 2) as avg_communication,
                        ROUND(AVG(qm.pain_management_score), 2) as avg_pain_mgmt
                    FROM admissions a
                    JOIN quality_metrics qm ON a.admission_id = qm.admission_id
                    WHERE qm.survey_completion_date >= CURRENT_DATE - INTERVAL '90 days'
                    GROUP BY a.department
                    ORDER BY avg_satisfaction DESC
                """
            },
            {
                "name": "DAILY ADMISSION VOLUME TREND (LAST 30 DAYS)",
                "query": """
                    SELECT 
                        admission_date::DATE as admission_day,
                        COUNT(*) as daily_admissions,
                        EXTRACT(DOW FROM admission_date) as day_of_week
                    FROM admissions 
                    WHERE admission_date >= CURRENT_DATE - INTERVAL '30 days'
                    GROUP BY admission_date::DATE
                    ORDER BY admission_day DESC
                """
            },
            {
                "name": "LENGTH OF STAY DISTRIBUTION BY DEPARTMENT",
                "query": """
                    SELECT 
                        department,
                        COUNT(*) as total_cases,
                        MIN(length_of_stay) as min_los,
                        ROUND(AVG(length_of_stay), 1) as avg_los,
                        MAX(length_of_stay) as max_los,
                        COUNT(CASE WHEN length_of_stay <= 2 THEN 1 END) as short_stay_count,
                        COUNT(CASE WHEN length_of_stay > 7 THEN 1 END) as long_stay_count
                    FROM admissions 
                    WHERE discharge_date IS NOT NULL
                    GROUP BY department
                    ORDER BY avg_los DESC
                """
            },
            {
                "name": "REVENUE ANALYSIS BY INSURANCE TYPE",
                "query": """
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
                    ORDER BY total_revenue DESC
                """
            },
            {
                "name": "HIGH-VOLUME PHYSICIANS",
                "query": """
                    SELECT 
                        attending_physician as physician_name,
                        COUNT(*) as total_cases,
                        ROUND(AVG(length_of_stay), 1) as avg_los,
                        COUNT(CASE WHEN discharge_date IS NULL THEN 1 END) as current_patients
                    FROM admissions 
                    WHERE admission_date >= CURRENT_DATE - INTERVAL '90 days'
                    GROUP BY attending_physician
                    HAVING COUNT(*) >= 5
                    ORDER BY total_cases DESC
                """
            },
            {
                "name": "WEEKEND VS WEEKDAY ADMISSIONS",
                "query": """
                    SELECT 
                        CASE 
                            WHEN EXTRACT(DOW FROM admission_date) IN (0, 6) THEN 'Weekend'
                            ELSE 'Weekday'
                        END as day_type,
                        COUNT(*) as admission_count,
                        ROUND(AVG(length_of_stay), 1) as avg_los,
                        ROUND(COUNT(*) * 100.0 / (
                            SELECT COUNT(*) FROM admissions 
                            WHERE admission_date >= CURRENT_DATE - INTERVAL '90 days'
                        ), 1) as percentage
                    FROM admissions 
                    WHERE admission_date >= CURRENT_DATE - INTERVAL '90 days'
                    GROUP BY day_type
                """
            },
            {
                "name": "EMERGENCY VS ELECTIVE ADMISSIONS BY MONTH",
                "query": """
                    SELECT 
                        TO_CHAR(admission_date, 'YYYY-MM') as month,
                        admission_type,
                        COUNT(*) as admission_count,
                        ROUND(AVG(length_of_stay), 1) as avg_los,
                        ROUND(AVG(fd.net_revenue), 2) as avg_revenue
                    FROM admissions a
                    JOIN financial_data fd ON a.admission_id = fd.admission_id
                    WHERE admission_date >= CURRENT_DATE - INTERVAL '12 months'
                    GROUP BY TO_CHAR(admission_date, 'YYYY-MM'), admission_type
                    ORDER BY month DESC, admission_type
                """
            },
            {
                "name": "PATIENT AGE DISTRIBUTION BY DIAGNOSIS",
                "query": """
                    SELECT 
                        d.diagnosis_description,
                        ROUND(AVG(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM p.date_of_birth)), 1) as avg_age,
                        COUNT(*) as patient_count,
                        MIN(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM p.date_of_birth)) as min_age,
                        MAX(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM p.date_of_birth)) as max_age
                    FROM diagnoses d
                    JOIN admissions a ON d.admission_id = a.admission_id
                    JOIN patients p ON a.patient_id = p.patient_id
                    WHERE d.diagnosis_type = 'Primary'
                      AND p.date_of_birth IS NOT NULL
                    GROUP BY d.diagnosis_description
                    ORDER BY patient_count DESC
                """
            },
            {
                "name": "ROOM UTILIZATION ANALYSIS",
                "query": """
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
                    LIMIT 20
                """
            },
            {
                "name": "PROCEDURE COST ANALYSIS",
                "query": """
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
                    LIMIT 15
                """
            },
            {
                "name": "FINANCIAL PERFORMANCE SUMMARY",
                "query": """
                    SELECT 
                        TO_CHAR(a.admission_date, 'YYYY-MM') as month,
                        COUNT(*) as total_admissions,
                        ROUND(SUM(fd.total_charges), 2) as total_charges,
                        ROUND(SUM(fd.insurance_payment), 2) as insurance_payments,
                        ROUND(SUM(fd.patient_payment), 2) as patient_payments,
                        ROUND(SUM(fd.net_revenue), 2) as net_revenue,
                        ROUND(AVG(fd.net_revenue), 2) as avg_revenue_per_case
                    FROM admissions a
                    JOIN financial_data fd ON a.admission_id = fd.admission_id
                    WHERE a.admission_date >= CURRENT_DATE - INTERVAL '12 months'
                    GROUP BY TO_CHAR(a.admission_date, 'YYYY-MM')
                    ORDER BY month DESC
                """
            }
        ]
        
        # Execute each query
        for i, query_info in enumerate(analytics_queries, 1):
            try:
                print(f"\n{'='*60}")
                print(f"QUERY {i}: {query_info['name']}")
                print(f"{'='*60}")
                
                # Execute query
                df = pd.read_sql_query(query_info['query'], engine)
                
                if not df.empty:
                    print(f"Results: {len(df)} rows")
                    print("-" * 60)
                    print(df.to_string(index=False))
                else:
                    print("No results found")
                    
            except Exception as e:
                print(f"Error executing query {i}: {str(e)}")
                continue
        
        print(f"\n{'='*80}")
        print("POSTGRESQL ANALYTICS COMPLETED SUCCESSFULLY!")
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        sys.exit(1)

def run_specific_query(query_number):
    """Run a specific query by number"""
    
    try:
        engine = get_postgresql_engine()
        
        # Define queries (same as above)
        analytics_queries = [
            {
                "name": "CURRENT PATIENT CENSUS BY DEPARTMENT",
                "query": """
                    SELECT
                        department,
                        COUNT(*) as current_patients,
                        ROUND(AVG(CURRENT_DATE - admission_date), 1) as avg_days_admitted
                    FROM admissions 
                    WHERE discharge_date IS NULL
                    GROUP BY department
                    ORDER BY current_patients DESC
                """
            },
            {
                "name": "MONTHLY ADMISSION TRENDS (LAST 12 MONTHS)",
                "query": """
                    SELECT 
                        TO_CHAR(admission_date, 'YYYY-MM') as month,
                        COUNT(*) as admissions,
                        ROUND(AVG(length_of_stay), 1) as avg_los
                    FROM admissions 
                    WHERE admission_date >= CURRENT_DATE - INTERVAL '12 months'
                    GROUP BY TO_CHAR(admission_date, 'YYYY-MM')
                    ORDER BY month
                """
            },
            {
                "name": "TOP DIAGNOSES BY VOLUME",
                "query": """
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
                    LIMIT 20
                """
            },
            {
                "name": "READMISSION ANALYSIS (LAST 30 DAYS)",
                "query": """
                    SELECT 
                        a.department,
                        COUNT(DISTINCT a.admission_id) as total_discharges,
                        COUNT(r.readmission_id) as readmissions,
                        ROUND(
                            CASE 
                                WHEN COUNT(DISTINCT a.admission_id) > 0 THEN
                                    (COUNT(r.readmission_id)::DECIMAL * 100.0 / COUNT(DISTINCT a.admission_id))
                                ELSE 0 
                            END, 2
                        ) as readmission_rate
                    FROM admissions a
                    LEFT JOIN readmissions r ON a.admission_id = r.original_admission_id
                    WHERE a.discharge_date >= CURRENT_DATE - INTERVAL '30 days'
                      AND a.discharge_date IS NOT NULL
                    GROUP BY a.department
                    ORDER BY readmission_rate DESC
                """
            },
            {
                "name": "PATIENT SATISFACTION BY DEPARTMENT (LAST 90 DAYS)",
                "query": """
                    SELECT 
                        a.department,
                        COUNT(qm.metric_id) as surveys_completed,
                        ROUND(AVG(qm.patient_satisfaction_score), 2) as avg_satisfaction,
                        ROUND(AVG(qm.communication_score), 2) as avg_communication,
                        ROUND(AVG(qm.pain_management_score), 2) as avg_pain_mgmt
                    FROM admissions a
                    JOIN quality_metrics qm ON a.admission_id = qm.admission_id
                    WHERE qm.survey_completion_date >= CURRENT_DATE - INTERVAL '90 days'
                    GROUP BY a.department
                    ORDER BY avg_satisfaction DESC
                """
            },
            {
                "name": "DAILY ADMISSION VOLUME TREND (LAST 30 DAYS)",
                "query": """
                    SELECT 
                        admission_date::DATE as admission_day,
                        COUNT(*) as daily_admissions,
                        EXTRACT(DOW FROM admission_date) as day_of_week
                    FROM admissions 
                    WHERE admission_date >= CURRENT_DATE - INTERVAL '30 days'
                    GROUP BY admission_date::DATE
                    ORDER BY admission_day DESC
                """
            },
            {
                "name": "LENGTH OF STAY DISTRIBUTION BY DEPARTMENT",
                "query": """
                    SELECT 
                        department,
                        COUNT(*) as total_cases,
                        MIN(length_of_stay) as min_los,
                        ROUND(AVG(length_of_stay), 1) as avg_los,
                        MAX(length_of_stay) as max_los,
                        COUNT(CASE WHEN length_of_stay <= 2 THEN 1 END) as short_stay_count,
                        COUNT(CASE WHEN length_of_stay > 7 THEN 1 END) as long_stay_count
                    FROM admissions 
                    WHERE discharge_date IS NOT NULL
                    GROUP BY department
                    ORDER BY avg_los DESC
                """
            },
            {
                "name": "REVENUE ANALYSIS BY INSURANCE TYPE",
                "query": """
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
                    ORDER BY total_revenue DESC
                """
            },
            {
                "name": "HIGH-VOLUME PHYSICIANS",
                "query": """
                    SELECT 
                        attending_physician as physician_name,
                        COUNT(*) as total_cases,
                        ROUND(AVG(length_of_stay), 1) as avg_los,
                        COUNT(CASE WHEN discharge_date IS NULL THEN 1 END) as current_patients
                    FROM admissions 
                    WHERE admission_date >= CURRENT_DATE - INTERVAL '90 days'
                    GROUP BY attending_physician
                    HAVING COUNT(*) >= 5
                    ORDER BY total_cases DESC
                """
            },
            {
                "name": "WEEKEND VS WEEKDAY ADMISSIONS",
                "query": """
                    SELECT 
                        CASE 
                            WHEN EXTRACT(DOW FROM admission_date) IN (0, 6) THEN 'Weekend'
                            ELSE 'Weekday'
                        END as day_type,
                        COUNT(*) as admission_count,
                        ROUND(AVG(length_of_stay), 1) as avg_los,
                        ROUND(COUNT(*) * 100.0 / (
                            SELECT COUNT(*) FROM admissions 
                            WHERE admission_date >= CURRENT_DATE - INTERVAL '90 days'
                        ), 1) as percentage
                    FROM admissions 
                    WHERE admission_date >= CURRENT_DATE - INTERVAL '90 days'
                    GROUP BY day_type
                """
            },
            {
                "name": "EMERGENCY VS ELECTIVE ADMISSIONS BY MONTH",
                "query": """
                    SELECT 
                        TO_CHAR(admission_date, 'YYYY-MM') as month,
                        admission_type,
                        COUNT(*) as admission_count,
                        ROUND(AVG(length_of_stay), 1) as avg_los,
                        ROUND(AVG(fd.net_revenue), 2) as avg_revenue
                    FROM admissions a
                    JOIN financial_data fd ON a.admission_id = fd.admission_id
                    WHERE admission_date >= CURRENT_DATE - INTERVAL '12 months'
                    GROUP BY TO_CHAR(admission_date, 'YYYY-MM'), admission_type
                    ORDER BY month DESC, admission_type
                """
            },
            {
                "name": "PATIENT AGE DISTRIBUTION BY DIAGNOSIS",
                "query": """
                    SELECT 
                        d.diagnosis_description,
                        ROUND(AVG(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM p.date_of_birth)), 1) as avg_age,
                        COUNT(*) as patient_count,
                        MIN(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM p.date_of_birth)) as min_age,
                        MAX(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM p.date_of_birth)) as max_age
                    FROM diagnoses d
                    JOIN admissions a ON d.admission_id = a.admission_id
                    JOIN patients p ON a.patient_id = p.patient_id
                    WHERE d.diagnosis_type = 'Primary'
                      AND p.date_of_birth IS NOT NULL
                    GROUP BY d.diagnosis_description
                    ORDER BY patient_count DESC
                """
            },
            {
                "name": "ROOM UTILIZATION ANALYSIS",
                "query": """
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
                    LIMIT 20
                """
            },
            {
                "name": "PROCEDURE COST ANALYSIS",
                "query": """
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
                    LIMIT 15
                """
            },
            {
                "name": "FINANCIAL PERFORMANCE SUMMARY",
                "query": """
                    SELECT 
                        TO_CHAR(a.admission_date, 'YYYY-MM') as month,
                        COUNT(*) as total_admissions,
                        ROUND(SUM(fd.total_charges), 2) as total_charges,
                        ROUND(SUM(fd.insurance_payment), 2) as insurance_payments,
                        ROUND(SUM(fd.patient_payment), 2) as patient_payments,
                        ROUND(SUM(fd.net_revenue), 2) as net_revenue,
                        ROUND(AVG(fd.net_revenue), 2) as avg_revenue_per_case
                    FROM admissions a
                    JOIN financial_data fd ON a.admission_id = fd.admission_id
                    WHERE a.admission_date >= CURRENT_DATE - INTERVAL '12 months'
                    GROUP BY TO_CHAR(a.admission_date, 'YYYY-MM')
                    ORDER BY month DESC
                """
            }
        ]
        
        if 1 <= query_number <= len(analytics_queries):
            query_info = analytics_queries[query_number - 1]
            
            print(f"\n{'='*60}")
            print(f"EXECUTING: {query_info['name']}")
            print(f"{'='*60}")
            print(f"SQL Query:\n{query_info['query']}")
            print(f"\n{'='*60}")
            print("RESULTS:")
            print(f"{'='*60}")
            
            df = pd.read_sql_query(query_info['query'], engine)
            
            if not df.empty:
                print(f"Results: {len(df)} rows")
                print("-" * 60)
                print(df.to_string(index=False))
            else:
                print("No results found")
        else:
            print(f"Query number {query_number} not found. Available queries: 1-{len(analytics_queries)}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

def test_connection():
    """Test PostgreSQL connection"""
    
    try:
        engine = get_postgresql_engine()
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM patients"))
            patient_count = result.fetchone()[0]
            
            result = conn.execute(text("SELECT COUNT(*) FROM admissions"))
            admission_count = result.fetchone()[0]
            
            print("✅ PostgreSQL connection successful!")
            print(f"   Patients: {patient_count:,}")
            print(f"   Admissions: {admission_count:,}")
            
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            test_connection()
        elif sys.argv[1].isdigit():
            run_specific_query(int(sys.argv[1]))
        else:
            print("Usage:")
            print("  python postgresql_analytics_queries.py          # Run all queries")
            print("  python postgresql_analytics_queries.py --test   # Test connection")
            print("  python postgresql_analytics_queries.py <number> # Run specific query")
    else:
        run_postgresql_analytics()
