# Python script to create SQLite database
import sqlite3
import pandas as pd
from datetime import datetime
import re

def create_healthcare_database():
    """Create SQLite database and load healthcare data"""
    
    # Create database connection
    conn = sqlite3.connect('healthcare_analytics.db')
    cursor = conn.cursor()
    
    print("Creating database schema...")
    
    # Execute schema creation
    with open('healthcare_schema_sqlite.sql', 'r') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    print("Loading healthcare dataset...")
    
    # Load CSV data
    df = pd.read_csv('healthcare_dataset.csv')
    print(f"Loaded {len(df)} records from CSV")
    
    # Clean and prepare data
    df_clean = clean_dataframe(df)
    
    # Insert data into tables
    insert_data_to_tables(cursor, df_clean)
    
    conn.commit()
    conn.close()
    
    print("Database created successfully!")
    print("Database file: healthcare_analytics.db")

def convert_to_sqlite_syntax(sql_content):
    """Convert PostgreSQL syntax to SQLite compatible syntax"""
    
    # Replace PostgreSQL specific syntax with SQLite equivalents
    sql_content = sql_content.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
    sql_content = sql_content.replace('VARCHAR', 'TEXT')
    sql_content = sql_content.replace('SERIAL', 'INTEGER')
    
    # Remove GENERATED ALWAYS AS clauses (not supported in SQLite)
    sql_content = re.sub(r'GENERATED ALWAYS AS \(.*?\) STORED,?', '', sql_content, flags=re.DOTALL)
    
    # Remove REFERENCES with SERIAL (will be handled manually)
    sql_content = re.sub(r'REFERENCES \w+\(\w+\)', '', sql_content)
    
    # Fix the financial_data table - remove the computed column
    sql_content = re.sub(r',\s*net_revenue\s+DECIMAL\(12,2\)\s+GENERATED ALWAYS AS \(.*?\) STORED', '', sql_content, flags=re.DOTALL)
    
    # Add net_revenue as a regular column
    sql_content = sql_content.replace('write_off_amount DECIMAL(12,2),', 'write_off_amount DECIMAL(12,2), net_revenue DECIMAL(12,2),')
    
    # Fix vital_signs table - remove computed BMI column
    sql_content = re.sub(r',\s*bmi\s+DECIMAL\(4,2\)\s+GENERATED ALWAYS AS \(.*?\) STORED', '', sql_content, flags=re.DOTALL)
    
    return sql_content

def clean_dataframe(df):
    """Clean and prepare the dataframe for database insertion"""
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Clean column names
    df_clean.columns = df_clean.columns.str.strip()
    
    # Handle missing values
    df_clean = df_clean.fillna('')
    
    # Convert date columns
    date_columns = ['Date of Admission', 'Discharge Date']
    for col in date_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce').dt.date
    
    # Clean gender values
    if 'Gender' in df_clean.columns:
        df_clean['Gender'] = df_clean['Gender'].str.upper().map({
            'MALE': 'M', 'FEMALE': 'F'
        }).fillna('Unknown')
    
    # Clean admission type
    if 'Admission Type' in df_clean.columns:
        df_clean['Admission Type'] = df_clean['Admission Type'].str.title()
    
    # Convert billing amount to numeric
    if 'Billing Amount' in df_clean.columns:
        df_clean['Billing Amount'] = pd.to_numeric(df_clean['Billing Amount'], errors='coerce')
    
    return df_clean

def insert_data_to_tables(cursor, df):
    """Insert data into the appropriate tables"""
    
    # Create unique patient IDs and insert patients
    print("Inserting patients...")
    patients_data = []
    patient_id_map = {}  # Map name to patient_id
    
    for idx, row in df.iterrows():
        # Create unique patient ID from name
        name = row['Name']
        if name not in patient_id_map:
            patient_id = f"P{idx+1:06d}"
            patient_id_map[name] = patient_id
            
            # Extract first and last name
            name_parts = name.split()
            first_name = name_parts[0] if name_parts else ''
            last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            
            # Estimate date of birth from age
            current_year = datetime.now().year
            birth_year = current_year - int(row['Age']) if pd.notna(row['Age']) else None
            date_of_birth = f"{birth_year}-01-01" if birth_year else None
            
            patients_data.append((
                patient_id,
                first_name,
                last_name,
                date_of_birth,
                row['Gender'],
                row.get('Race', ''),
                row.get('Ethnicity', ''),
                row.get('Zip Code', ''),
                row['Insurance Provider'],
                datetime.now().date(),
                datetime.now().date()
            ))
    
    # Insert patients
    cursor.executemany('''
        INSERT INTO patients (patient_id, first_name, last_name, date_of_birth, 
                             gender, race, ethnicity, zip_code, insurance_type, 
                             created_date, updated_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', patients_data)
    
    print(f"Inserted {len(patients_data)} patients")
    
    # Insert admissions
    print("Inserting admissions...")
    admissions_data = []
    
    for idx, row in df.iterrows():
        patient_id = patient_id_map[row['Name']]
        admission_id = idx + 1
        
        # Calculate length of stay
        length_of_stay = None
        if pd.notna(row['Date of Admission']) and pd.notna(row['Discharge Date']):
            try:
                admission_date = pd.to_datetime(row['Date of Admission'])
                discharge_date = pd.to_datetime(row['Discharge Date'])
                length_of_stay = (discharge_date - admission_date).days
            except:
                length_of_stay = None
        
        admissions_data.append((
            admission_id,
            patient_id,
            row['Date of Admission'],
            row['Discharge Date'],
            row['Admission Type'],
            'Home',  # Default discharge status
            length_of_stay,
            'General',  # Default department
            row['Doctor'],
            row['Room Number'],
            datetime.now().date()
        ))
    
    # Insert admissions
    cursor.executemany('''
        INSERT INTO admissions (admission_id, patient_id, admission_date, discharge_date,
                               admission_type, discharge_status, length_of_stay,
                               department, attending_physician, room_number, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', admissions_data)
    
    print(f"Inserted {len(admissions_data)} admissions")
    
    # Insert diagnoses
    print("Inserting diagnoses...")
    diagnoses_data = []
    
    for idx, row in df.iterrows():
        admission_id = idx + 1
        
        # Create ICD-10 like code from medical condition
        condition = row['Medical Condition']
        icd_code = f"ICD10_{condition.upper().replace(' ', '_')[:10]}"
        
        diagnoses_data.append((
            admission_id,
            icd_code,
            condition,
            'Primary',
            3,  # Default severity level
            False  # Default chronic condition
        ))
    
    # Insert diagnoses
    cursor.executemany('''
        INSERT INTO diagnoses (admission_id, diagnosis_code, diagnosis_description,
                              diagnosis_type, severity_level, chronic_condition)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', diagnoses_data)
    
    print(f"Inserted {len(diagnoses_data)} diagnoses")
    
    # Insert financial data
    print("Inserting financial data...")
    financial_data = []
    
    for idx, row in df.iterrows():
        admission_id = idx + 1
        total_charges = row['Billing Amount'] if pd.notna(row['Billing Amount']) else 0
        
        # Estimate other financial fields
        insurance_payment = total_charges * 0.8  # Assume 80% insurance coverage
        patient_payment = total_charges * 0.15   # Assume 15% patient responsibility
        adjustment_amount = total_charges * 0.05  # Assume 5% adjustments
        
        financial_data.append((
            admission_id,
            total_charges,
            insurance_payment,
            patient_payment,
            adjustment_amount,
            0,  # write_off_amount
            insurance_payment + patient_payment,  # net_revenue
            row['Date of Admission'],
            row['Discharge Date']
        ))
    
    # Insert financial data
    cursor.executemany('''
        INSERT INTO financial_data (admission_id, total_charges, insurance_payment,
                                   patient_payment, adjustment_amount, write_off_amount,
                                   net_revenue, billing_date, payment_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', financial_data)
    
    print(f"Inserted {len(financial_data)} financial records")
    
    # Insert procedures (using medication as procedure)
    print("Inserting procedures...")
    procedures_data = []
    
    for idx, row in df.iterrows():
        admission_id = idx + 1
        
        procedures_data.append((
            admission_id,
            f"CPT_{row['Medication'].upper().replace(' ', '_')[:10]}",
            f"Medication: {row['Medication']}",
            row['Date of Admission'],
            row['Doctor'],
            30,  # Default duration in minutes
            row['Billing Amount'] * 0.1 if pd.notna(row['Billing Amount']) else 0  # 10% of total charges
        ))
    
    # Insert procedures
    cursor.executemany('''
        INSERT INTO procedures (admission_id, procedure_code, procedure_description,
                               procedure_date, performing_physician, procedure_duration, procedure_cost)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', procedures_data)
    
    print(f"Inserted {len(procedures_data)} procedures")

if __name__ == "__main__":
    create_healthcare_database()
