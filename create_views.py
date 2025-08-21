#!/usr/bin/env python3
"""
Create Database Views
Creates useful views for healthcare analytics
"""

import sqlite3
import sys

def create_views():
    """Create all database views"""
    
    try:
        # Connect to database
        conn = sqlite3.connect('healthcare_analytics.db')
        cursor = conn.cursor()
        
        print("Creating database views...")
        
        # Read and execute views
        with open('Views for common queries.sql', 'r') as f:
            views_sql = f.read()
            cursor.executescript(views_sql)
        
        conn.commit()
        conn.close()
        
        print("✅ Database views created successfully!")
        print("\nAvailable views:")
        print("1. patient_summary - Patient demographics and admission history")
        print("2. department_performance - Department metrics and performance")
        print("3. monthly_metrics - Monthly admission and financial trends")
        print("4. high_risk_patients - Patients with high readmission risk")
        print("5. current_census - Current patient census by department")
        print("6. top_diagnoses - Most common diagnoses with metrics")
        print("7. physician_performance - Physician workload and performance")
        print("8. financial_summary - Monthly financial performance")
        
        print("\nExample usage:")
        print("SELECT * FROM current_census;")
        print("SELECT * FROM top_diagnoses LIMIT 10;")
        print("SELECT * FROM physician_performance WHERE total_cases > 10;")
        
    except Exception as e:
        print(f"❌ Error creating views: {str(e)}")
        sys.exit(1)

def list_views():
    """List all available views"""
    
    try:
        conn = sqlite3.connect('healthcare_analytics.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
        views = cursor.fetchall()
        
        print("Available database views:")
        print("=" * 40)
        
        for i, view in enumerate(views, 1):
            print(f"{i}. {view[0]}")
            
        conn.close()
        
    except Exception as e:
        print(f"Error listing views: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_views()
    else:
        create_views()
