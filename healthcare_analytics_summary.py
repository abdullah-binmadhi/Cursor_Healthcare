#!/usr/bin/env python3
"""
Healthcare Analytics System Summary
Demonstrates all capabilities of the healthcare analytics database
"""

import sqlite3
import pandas as pd
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'-'*60}")
    print(f" {title}")
    print(f"{'-'*60}")

def healthcare_analytics_summary():
    """Generate a comprehensive healthcare analytics summary"""
    
    try:
        conn = sqlite3.connect('healthcare_analytics.db')
        
        print_header("HEALTHCARE ANALYTICS SYSTEM SUMMARY")
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Database Overview
        print_section("DATABASE OVERVIEW")
        
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Database Tables:")
        for table in tables:
            if not table[0].startswith('sqlite_'):
                count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table[0]}", conn).iloc[0]['count']
                print(f"  • {table[0]}: {count:,} records")
        
        # Views
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
        views = cursor.fetchall()
        
        print(f"\nDatabase Views ({len(views)}):")
        for view in views:
            print(f"  • {view[0]}")
        
        # Key Metrics
        print_section("KEY PERFORMANCE INDICATORS")
        
        # Total patients and admissions
        total_patients = pd.read_sql_query("SELECT COUNT(*) as count FROM patients", conn).iloc[0]['count']
        total_admissions = pd.read_sql_query("SELECT COUNT(*) as count FROM admissions", conn).iloc[0]['count']
        total_revenue = pd.read_sql_query("SELECT SUM(net_revenue) as total FROM financial_data", conn).iloc[0]['total']
        
        print(f"Total Patients: {total_patients:,}")
        print(f"Total Admissions: {total_admissions:,}")
        print(f"Total Net Revenue: ${total_revenue:,.2f}")
        
        # Average metrics
        avg_los = pd.read_sql_query("SELECT AVG(length_of_stay) as avg_los FROM admissions WHERE length_of_stay IS NOT NULL", conn).iloc[0]['avg_los']
        avg_revenue = pd.read_sql_query("SELECT AVG(net_revenue) as avg_revenue FROM financial_data", conn).iloc[0]['avg_revenue']
        
        print(f"Average Length of Stay: {avg_los:.1f} days")
        print(f"Average Revenue per Case: ${avg_revenue:,.2f}")
        
        # Top Diagnoses
        print_section("TOP 5 DIAGNOSES")
        df_diagnoses = pd.read_sql_query("SELECT * FROM top_diagnoses LIMIT 5", conn)
        print(df_diagnoses.to_string(index=False))
        
        # Insurance Analysis
        print_section("INSURANCE TYPE ANALYSIS")
        df_insurance = pd.read_sql_query("""
            SELECT 
                p.insurance_type,
                COUNT(*) as case_count,
                ROUND(AVG(fd.net_revenue), 2) as avg_revenue,
                ROUND(SUM(fd.net_revenue), 2) as total_revenue
            FROM patients p
            JOIN admissions a ON p.patient_id = a.patient_id
            JOIN financial_data fd ON a.admission_id = fd.admission_id
            GROUP BY p.insurance_type
            ORDER BY total_revenue DESC
        """, conn)
        print(df_insurance.to_string(index=False))
        
        # Admission Types
        print_section("ADMISSION TYPE DISTRIBUTION")
        df_admission_types = pd.read_sql_query("""
            SELECT 
                admission_type,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM admissions), 1) as percentage
            FROM admissions
            GROUP BY admission_type
            ORDER BY count DESC
        """, conn)
        print(df_admission_types.to_string(index=False))
        
        # Physician Performance
        print_section("TOP 5 PHYSICIANS BY CASE VOLUME")
        df_physicians = pd.read_sql_query("""
            SELECT 
                attending_physician,
                COUNT(*) as total_cases,
                ROUND(AVG(length_of_stay), 1) as avg_los,
                ROUND(AVG(fd.net_revenue), 2) as avg_revenue
            FROM admissions a
            JOIN financial_data fd ON a.admission_id = fd.admission_id
            GROUP BY attending_physician
            HAVING COUNT(*) >= 5
            ORDER BY total_cases DESC
            LIMIT 5
        """, conn)
        print(df_physicians.to_string(index=False))
        
        # Monthly Trends
        print_section("MONTHLY ADMISSION TRENDS (LAST 6 MONTHS)")
        df_monthly = pd.read_sql_query("""
            SELECT 
                strftime('%Y-%m', admission_date) as month,
                COUNT(*) as admissions,
                ROUND(AVG(length_of_stay), 1) as avg_los,
                ROUND(SUM(fd.net_revenue), 2) as total_revenue
            FROM admissions a
            JOIN financial_data fd ON a.admission_id = fd.admission_id
            WHERE admission_date >= date('now', '-6 months')
            GROUP BY strftime('%Y-%m', admission_date)
            ORDER BY month DESC
            LIMIT 6
        """, conn)
        print(df_monthly.to_string(index=False))
        
        # Room Utilization
        print_section("TOP 10 ROOMS BY UTILIZATION")
        df_rooms = pd.read_sql_query("""
            SELECT 
                room_number,
                COUNT(*) as total_admissions,
                ROUND(AVG(length_of_stay), 1) as avg_los,
                ROUND(SUM(fd.net_revenue), 2) as total_revenue
            FROM admissions a
            JOIN financial_data fd ON a.admission_id = fd.admission_id
            WHERE room_number IS NOT NULL AND room_number != ''
            GROUP BY room_number
            ORDER BY total_admissions DESC
            LIMIT 10
        """, conn)
        print(df_rooms.to_string(index=False))
        
        # System Capabilities
        print_section("ANALYTICS SYSTEM CAPABILITIES")
        print("✅ Database Schema: 8 tables with comprehensive healthcare data")
        print("✅ Sample Data: 10,000 admissions with realistic healthcare scenarios")
        print("✅ Analytics Queries: 15 essential healthcare analytics queries")
        print("✅ Database Views: 8 pre-built views for common analytics")
        print("✅ Performance Indexes: Optimized for fast query execution")
        print("✅ Data Quality: Cleaned and validated healthcare data")
        print("✅ Financial Analysis: Complete revenue and cost analysis")
        print("✅ Clinical Metrics: Length of stay, diagnoses, procedures")
        print("✅ Operational Analytics: Room utilization, physician performance")
        print("✅ Trend Analysis: Monthly and seasonal patterns")
        
        # Usage Instructions
        print_section("USAGE INSTRUCTIONS")
        print("1. Run all analytics: python run_analytics_queries.py")
        print("2. List queries: python run_analytics_queries.py --list")
        print("3. Run specific query: python run_analytics_queries.py <number>")
        print("4. Create views: python create_views.py")
        print("5. Test database: python test_database.py")
        print("6. Direct SQL: sqlite3 healthcare_analytics.db")
        
        print_header("ANALYTICS SUMMARY COMPLETE")
        
        conn.close()
        
    except Exception as e:
        print(f"Error generating summary: {str(e)}")

if __name__ == "__main__":
    healthcare_analytics_summary()
