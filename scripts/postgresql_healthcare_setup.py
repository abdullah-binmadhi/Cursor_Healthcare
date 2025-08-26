#!/usr/bin/env python3
"""
PostgreSQL Healthcare Analytics Setup
Creates and populates a PostgreSQL database for healthcare analytics
"""

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text
import numpy as np
from datetime import datetime
import sys
import os

def create_postgresql_schema(engine):
    """Create PostgreSQL schema for healthcare analytics"""
    
    schema_sql = """
    -- ====================
    -- POSTGRESQL HEALTHCARE SCHEMA
    -- ====================
    
    -- 1. PATIENTS TABLE
    CREATE TABLE IF NOT EXISTS patients (
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

    -- 2. ADMISSIONS TABLE
    CREATE TABLE IF NOT EXISTS admissions (
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

    -- 3. DIAGNOSES TABLE
    CREATE TABLE IF NOT EXISTS diagnoses (
        diagnosis_id SERIAL PRIMARY KEY,
        admission_id INTEGER REFERENCES admissions(admission_id),
        diagnosis_code VARCHAR(20),
        diagnosis_description TEXT,
        diagnosis_type VARCHAR(20) CHECK (diagnosis_type IN ('Primary', 'Secondary', 'Comorbidity')),
        severity_level INTEGER CHECK (severity_level BETWEEN 1 AND 5),
        chronic_condition BOOLEAN DEFAULT FALSE
    );

    -- 4. PROCEDURES TABLE
    CREATE TABLE IF NOT EXISTS procedures (
        procedure_id SERIAL PRIMARY KEY,
        admission_id INTEGER REFERENCES admissions(admission_id),
        procedure_code VARCHAR(20),
        procedure_description TEXT,
        procedure_date DATE,
        performing_physician VARCHAR(100),
        procedure_duration INTEGER,
        procedure_cost DECIMAL(10,2)
    );

    -- 5. FINANCIAL DATA TABLE
    CREATE TABLE IF NOT EXISTS financial_data (
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

    -- 6. READMISSIONS TABLE
    CREATE TABLE IF NOT EXISTS readmissions (
        readmission_id SERIAL PRIMARY KEY,
        original_admission_id INTEGER REFERENCES admissions(admission_id),
        readmission_admission_id INTEGER REFERENCES admissions(admission_id),
        days_between_admissions INTEGER,
        same_diagnosis BOOLEAN,
        preventable_flag BOOLEAN,
        readmission_type VARCHAR(50) CHECK (readmission_type IN ('Planned', 'Unplanned', 'Related', 'Unrelated'))
    );

    -- 7. QUALITY METRICS TABLE
    CREATE TABLE IF NOT EXISTS quality_metrics (
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

    -- 8. VITAL SIGNS TABLE
    CREATE TABLE IF NOT EXISTS vital_signs (
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

    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_admissions_patient_id ON admissions(patient_id);
    CREATE INDEX IF NOT EXISTS idx_admissions_hospital_id ON admissions(admission_id);
    CREATE INDEX IF NOT EXISTS idx_admissions_date ON admissions(admission_date);
    CREATE INDEX IF NOT EXISTS idx_diagnoses_admission_id ON diagnoses(admission_id);
    CREATE INDEX IF NOT EXISTS idx_treatments_admission_id ON procedures(admission_id);
    CREATE INDEX IF NOT EXISTS idx_financial_admission_id ON financial_data(admission_id);
    CREATE INDEX IF NOT EXISTS idx_vital_signs_admission_id ON vital_signs(admission_id);
    """
    
    try:
        with engine.connect() as conn:
            conn.execute(text(schema_sql))
            conn.commit()
        print("✅ PostgreSQL schema created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating schema: {str(e)}")
        return False

def prepare_healthcare_data(df):
    """Clean and prepare healthcare data for PostgreSQL"""
    
    print("Cleaning and preparing data...")
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Clean column names
    df_clean.columns = df_clean.columns.str.strip()
    
    # Create unique patient IDs if not present
    if 'patient_id' not in df_clean.columns:
        df_clean['patient_id'] = [f"P{i+1:06d}" for i in range(len(df_clean))]
    
    # Clean patient IDs
    df_clean['patient_id'] = df_clean['patient_id'].astype(str).str.strip()
    
    # Extract first and last name from Name column
    if 'Name' in df_clean.columns and 'first_name' not in df_clean.columns:
        name_parts = df_clean['Name'].str.split(' ', n=1, expand=True)
        df_clean['first_name'] = name_parts[0]
        df_clean['last_name'] = name_parts[1].fillna('')
    
    # Convert dates
    date_columns = ['Date of Admission', 'Discharge Date']
    for col in date_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
    
    # Handle missing values
    if 'Gender' in df_clean.columns:
        df_clean['Gender'] = df_clean['Gender'].str.upper().map({
            'MALE': 'M', 'FEMALE': 'F'
        }).fillna('Unknown')
    
    # Create calculated fields
    if 'Date of Admission' in df_clean.columns and 'Discharge Date' in df_clean.columns:
        df_clean['length_of_stay'] = (df_clean['Discharge Date'] - df_clean['Date of Admission']).dt.days
    
    # Clean admission type
    if 'Admission Type' in df_clean.columns:
        df_clean['Admission Type'] = df_clean['Admission Type'].str.title()
    
    # Convert billing amount to numeric
    if 'Billing Amount' in df_clean.columns:
        df_clean['Billing Amount'] = pd.to_numeric(df_clean['Billing Amount'], errors='coerce')
    
    print(f"✅ Data cleaned: {len(df_clean)} records")
    return df_clean

def load_data_to_postgresql(engine, df_clean):
    """Load cleaned data into PostgreSQL tables"""
    
    print("Loading data into PostgreSQL...")
    
    try:
        # Create patients table data
        patients_data = []
        patient_id_map = {}
        
        for idx, row in df_clean.iterrows():
            name = row['Name']
            if name not in patient_id_map:
                patient_id = f"P{idx+1:06d}"
                patient_id_map[name] = patient_id
                
                # Estimate date of birth from age
                current_year = datetime.now().year
                birth_year = current_year - int(row['Age']) if pd.notna(row['Age']) else None
                date_of_birth = f"{birth_year}-01-01" if birth_year else None
                
                patients_data.append({
                    'patient_id': patient_id,
                    'first_name': row.get('first_name', ''),
                    'last_name': row.get('last_name', ''),
                    'date_of_birth': date_of_birth,
                    'gender': row['Gender'],
                    'race': row.get('Race', ''),
                    'ethnicity': row.get('Ethnicity', ''),
                    'zip_code': row.get('Zip Code', ''),
                    'insurance_type': row['Insurance Provider'],
                    'created_date': datetime.now(),
                    'updated_date': datetime.now()
                })
        
        # Create admissions table data
        admissions_data = []
        
        for idx, row in df_clean.iterrows():
            patient_id = patient_id_map[row['Name']]
            
            admissions_data.append({
                'patient_id': patient_id,
                'admission_date': row['Date of Admission'],
                'discharge_date': row['Discharge Date'],
                'admission_type': row['Admission Type'],
                'discharge_status': 'Home',  # Default
                'department': 'General',  # Default
                'attending_physician': row['Doctor'],
                'room_number': row['Room Number'],
                'created_date': datetime.now()
            })
        
        # Create diagnoses table data
        diagnoses_data = []
        
        for idx, row in df_clean.iterrows():
            condition = row['Medical Condition']
            icd_code = f"ICD10_{condition.upper().replace(' ', '_')[:10]}"
            
            diagnoses_data.append({
                'admission_id': idx + 1,
                'diagnosis_code': icd_code,
                'diagnosis_description': condition,
                'diagnosis_type': 'Primary',
                'severity_level': 3,
                'chronic_condition': False
            })
        
        # Create financial data
        financial_data = []
        
        for idx, row in df_clean.iterrows():
            total_charges = row['Billing Amount'] if pd.notna(row['Billing Amount']) else 0
            
            financial_data.append({
                'admission_id': idx + 1,
                'total_charges': total_charges,
                'insurance_payment': total_charges * 0.8,
                'patient_payment': total_charges * 0.15,
                'adjustment_amount': total_charges * 0.05,
                'write_off_amount': 0,
                'billing_date': row['Date of Admission'],
                'payment_date': row['Discharge Date']
            })
        
        # Create procedures data
        procedures_data = []
        
        for idx, row in df_clean.iterrows():
            procedures_data.append({
                'admission_id': idx + 1,
                'procedure_code': f"CPT_{row['Medication'].upper().replace(' ', '_')[:10]}",
                'procedure_description': f"Medication: {row['Medication']}",
                'procedure_date': row['Date of Admission'],
                'performing_physician': row['Doctor'],
                'procedure_duration': 30,
                'procedure_cost': row['Billing Amount'] * 0.1 if pd.notna(row['Billing Amount']) else 0
            })
        
        # Load data into PostgreSQL
        print("Loading patients...")
        patients_df = pd.DataFrame(patients_data)
        patients_df.to_sql('patients', engine, if_exists='append', index=False, method='multi')
        
        print("Loading admissions...")
        admissions_df = pd.DataFrame(admissions_data)
        admissions_df.to_sql('admissions', engine, if_exists='append', index=False, method='multi')
        
        print("Loading diagnoses...")
        diagnoses_df = pd.DataFrame(diagnoses_data)
        diagnoses_df.to_sql('diagnoses', engine, if_exists='append', index=False, method='multi')
        
        print("Loading financial data...")
        financial_df = pd.DataFrame(financial_data)
        financial_df.to_sql('financial_data', engine, if_exists='append', index=False, method='multi')
        
        print("Loading procedures...")
        procedures_df = pd.DataFrame(procedures_data)
        procedures_df.to_sql('procedures', engine, if_exists='append', index=False, method='multi')
        
        print("✅ Data loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        return False

def test_postgresql_connection(engine):
    """Test PostgreSQL connection and basic queries"""
    
    print("Testing PostgreSQL connection...")
    
    try:
        with engine.connect() as conn:
            # Test basic queries
            result = conn.execute(text("SELECT COUNT(*) FROM patients"))
            patient_count = result.fetchone()[0]
            
            result = conn.execute(text("SELECT COUNT(*) FROM admissions"))
            admission_count = result.fetchone()[0]
            
            result = conn.execute(text("SELECT COUNT(*) FROM financial_data"))
            financial_count = result.fetchone()[0]
            
            print(f"✅ Connection successful!")
            print(f"   Patients: {patient_count:,}")
            print(f"   Admissions: {admission_count:,}")
            print(f"   Financial Records: {financial_count:,}")
            
            # Test a sample analytics query
            result = conn.execute(text("""
                SELECT 
                    d.diagnosis_description,
                    COUNT(*) as case_count,
                    ROUND(AVG(a.length_of_stay), 1) as avg_los
                FROM diagnoses d
                JOIN admissions a ON d.admission_id = a.admission_id
                WHERE d.diagnosis_type = 'Primary'
                GROUP BY d.diagnosis_description
                ORDER BY case_count DESC
                LIMIT 5
            """))
            
            print("\nSample Analytics Query Results:")
            print("Top 5 Diagnoses:")
            for row in result:
                print(f"   {row[0]}: {row[1]} cases, {row[2]} avg LOS")
            
            return True
            
    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")
        return False

def main():
    """Main function to set up PostgreSQL healthcare analytics"""
    
    # PostgreSQL connection parameters
    # Update these with your actual PostgreSQL credentials
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'healthcare_analytics')
    
    # Create database connection string
    connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    print("=" * 80)
    print("POSTGRESQL HEALTHCARE ANALYTICS SETUP")
    print("=" * 80)
    print(f"Database: {DB_NAME}")
    print(f"Host: {DB_HOST}:{DB_PORT}")
    print(f"User: {DB_USER}")
    print()
    
    try:
        # Create engine
        engine = create_engine(connection_string)
        
        # Test connection
        with engine.connect() as conn:
            print("✅ PostgreSQL connection established!")
        
        # Load CSV data
        csv_file = 'healthcare_dataset.csv'
        if not os.path.exists(csv_file):
            print(f"❌ CSV file not found: {csv_file}")
            return
        
        print(f"Loading data from: {csv_file}")
        df = pd.read_csv(csv_file)
        print(f"Loaded {len(df)} records from CSV")
        
        # Create schema
        if not create_postgresql_schema(engine):
            return
        
        # Prepare data
        df_clean = prepare_healthcare_data(df)
        
        # Load data
        if not load_data_to_postgresql(engine, df_clean):
            return
        
        # Test connection and queries
        test_postgresql_connection(engine)
        
        print("\n" + "=" * 80)
        print("POSTGRESQL HEALTHCARE ANALYTICS SETUP COMPLETE!")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Connect to your PostgreSQL database")
        print("2. Run analytics queries using SQLAlchemy or psql")
        print("3. Create additional indexes for performance")
        print("4. Set up automated data loading processes")
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check PostgreSQL is running")
        print("2. Verify connection credentials")
        print("3. Ensure database exists")
        print("4. Check network connectivity")

if __name__ == "__main__":
    main()
