import sqlite3
import pandas as pd

def test_database():
    """Test the healthcare database with some sample queries"""
    
    conn = sqlite3.connect('healthcare_analytics.db')
    
    print("=== Healthcare Analytics Database Test ===\n")
    
    # Test 1: Check table structure
    print("1. Database Tables:")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(f"   - {table[0]}")
    
    print("\n2. Sample Data from Each Table:")
    
    # Test 2: Sample data from patients
    print("\n   Patients (first 3 records):")
    df_patients = pd.read_sql_query("SELECT * FROM patients LIMIT 3", conn)
    print(df_patients.to_string(index=False))
    
    # Test 3: Sample data from admissions
    print("\n   Admissions (first 3 records):")
    df_admissions = pd.read_sql_query("SELECT * FROM admissions LIMIT 3", conn)
    print(df_admissions.to_string(index=False))
    
    # Test 4: Sample data from diagnoses
    print("\n   Diagnoses (first 3 records):")
    df_diagnoses = pd.read_sql_query("SELECT * FROM diagnoses LIMIT 3", conn)
    print(df_diagnoses.to_string(index=False))
    
    # Test 5: Sample data from financial_data
    print("\n   Financial Data (first 3 records):")
    df_financial = pd.read_sql_query("SELECT * FROM financial_data LIMIT 3", conn)
    print(df_financial.to_string(index=False))
    
    # Test 6: Sample data from procedures
    print("\n   Procedures (first 3 records):")
    df_procedures = pd.read_sql_query("SELECT * FROM procedures LIMIT 3", conn)
    print(df_procedures.to_string(index=False))
    
    print("\n3. Database Statistics:")
    
    # Count records in each table
    for table in tables:
        table_name = table[0]
        count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table_name}", conn).iloc[0]['count']
        print(f"   {table_name}: {count:,} records")
    
    print("\n4. Sample Analytics Queries:")
    
    # Query 1: Average billing amount by admission type
    print("\n   Average Billing Amount by Admission Type:")
    df_avg_billing = pd.read_sql_query("""
        SELECT a.admission_type, 
               AVG(f.total_charges) as avg_charges,
               COUNT(*) as admission_count
        FROM admissions a
        JOIN financial_data f ON a.admission_id = f.admission_id
        GROUP BY a.admission_type
        ORDER BY avg_charges DESC
    """, conn)
    print(df_avg_billing.to_string(index=False))
    
    # Query 2: Top medical conditions
    print("\n   Top 5 Medical Conditions:")
    df_top_conditions = pd.read_sql_query("""
        SELECT diagnosis_description, COUNT(*) as count
        FROM diagnoses
        GROUP BY diagnosis_description
        ORDER BY count DESC
        LIMIT 5
    """, conn)
    print(df_top_conditions.to_string(index=False))
    
    # Query 3: Average length of stay by condition
    print("\n   Average Length of Stay by Medical Condition:")
    df_avg_los = pd.read_sql_query("""
        SELECT d.diagnosis_description,
               AVG(a.length_of_stay) as avg_length_of_stay,
               COUNT(*) as admission_count
        FROM admissions a
        JOIN diagnoses d ON a.admission_id = d.admission_id
        WHERE a.length_of_stay IS NOT NULL
        GROUP BY d.diagnosis_description
        ORDER BY avg_length_of_stay DESC
        LIMIT 5
    """, conn)
    print(df_avg_los.to_string(index=False))
    
    conn.close()
    print("\n=== Database test completed successfully! ===")

if __name__ == "__main__":
    test_database()
