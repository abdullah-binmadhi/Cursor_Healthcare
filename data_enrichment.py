#!/usr/bin/env python3
"""
Healthcare Data Enrichment
Populates missing data and creates additional data sources for healthcare analytics
"""

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import random
import json
from pathlib import Path

class HealthcareDataEnrichment:
    """Enriches healthcare data with missing information"""
    
    def __init__(self, csv_path='healthcare_dataset.csv', db_path='healthcare_analytics.db'):
        self.csv_path = csv_path
        self.db_path = db_path
        
        # Sample data for enrichment
        self.departments = [
            'Emergency Medicine', 'Cardiology', 'Orthopedics', 'Neurology', 
            'Oncology', 'Pediatrics', 'Internal Medicine', 'Surgery',
            'Psychiatry', 'Radiology', 'Anesthesiology', 'Obstetrics'
        ]
        
        self.physicians = [
            'Dr. Sarah Johnson', 'Dr. Michael Chen', 'Dr. Emily Rodriguez', 'Dr. David Kim',
            'Dr. Lisa Thompson', 'Dr. Robert Wilson', 'Dr. Jennifer Davis', 'Dr. Christopher Brown',
            'Dr. Amanda Garcia', 'Dr. James Miller', 'Dr. Michelle Lee', 'Dr. Thomas Anderson',
            'Dr. Rachel White', 'Dr. Daniel Martinez', 'Dr. Jessica Taylor'
        ]
        
        self.insurance_providers = [
            'Blue Cross Blue Shield', 'Aetna', 'Cigna', 'UnitedHealthcare',
            'Humana', 'Kaiser Permanente', 'Anthem', 'Medicare',
            'Medicaid', 'Tricare', 'Health Net', 'Molina Healthcare'
        ]
        
        self.medical_conditions = [
            'Hypertension', 'Diabetes Type 2', 'Coronary Artery Disease', 'Asthma',
            'Chronic Obstructive Pulmonary Disease', 'Heart Failure', 'Stroke',
            'Pneumonia', 'Urinary Tract Infection', 'Gastroenteritis',
            'Appendicitis', 'Gallbladder Disease', 'Kidney Stones', 'Migraine',
            'Depression', 'Anxiety', 'Osteoarthritis', 'Rheumatoid Arthritis'
        ]
        
        self.medications = [
            'Aspirin', 'Lisinopril', 'Metformin', 'Atorvastatin', 'Amlodipine',
            'Omeprazole', 'Albuterol', 'Ibuprofen', 'Acetaminophen', 'Warfarin',
            'Furosemide', 'Losartan', 'Carvedilol', 'Sertraline', 'Escitalopram',
            'Tramadol', 'Oxycodone', 'Morphine', 'Insulin', 'Glipizide'
        ]
        
        self.test_results = [
            'Normal', 'Abnormal', 'Inconclusive', 'Positive', 'Negative',
            'Elevated', 'Low', 'High', 'Borderline', 'Critical'
        ]
        
        self.blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        self.races = ['White', 'Black', 'Hispanic', 'Asian', 'Native American', 'Other']
        
        self.ethnicities = ['Non-Hispanic', 'Hispanic', 'Unknown']
        
        self.zip_codes = [
            '10001', '10002', '10003', '10004', '10005', '10006', '10007', '10008',
            '10009', '10010', '10011', '10012', '10013', '10014', '10015', '10016',
            '10017', '10018', '10019', '10020', '10021', '10022', '10023', '10024',
            '10025', '10026', '10027', '10028', '10029', '10030', '10031', '10032'
        ]
    
    def enrich_healthcare_data(self):
        """Enrich the healthcare dataset with missing data"""
        print("Loading healthcare dataset...")
        df = pd.read_csv(self.csv_path)
        
        print(f"Original dataset: {len(df)} records")
        print(f"Original columns: {list(df.columns)}")
        
        # Add missing columns with realistic data
        print("\nEnriching data...")
        
        # Add departments
        df['Department'] = np.random.choice(self.departments, len(df))
        
        # Add more detailed admission types
        admission_types = ['Emergency', 'Elective', 'Urgent', 'Transfer', 'Scheduled']
        df['Admission Type'] = np.random.choice(admission_types, len(df))
        
        # Add discharge status
        discharge_statuses = ['Home', 'Transfer', 'AMA', 'Expired', 'SNF', 'Rehabilitation']
        df['Discharge Status'] = np.random.choice(discharge_statuses, len(df))
        
        # Add race and ethnicity
        df['Race'] = np.random.choice(self.races, len(df))
        df['Ethnicity'] = np.random.choice(self.ethnicities, len(df))
        
        # Add zip codes
        df['Zip Code'] = np.random.choice(self.zip_codes, len(df))
        
        # Add more detailed blood types
        df['Blood Type'] = np.random.choice(self.blood_types, len(df))
        
        # Add room types
        room_types = ['Private', 'Semi-Private', 'ICU', 'CCU', 'NICU', 'PICU']
        df['Room Type'] = np.random.choice(room_types, len(df))
        
        # Add length of stay calculation
        df['Length of Stay'] = np.random.randint(1, 30, len(df))
        
        # Add severity scores
        df['Severity Score'] = np.random.randint(1, 6, len(df))
        
        # Add readmission flags
        df['Readmission'] = np.random.choice([True, False], len(df), p=[0.15, 0.85])
        
        # Add patient satisfaction scores
        df['Satisfaction Score'] = np.round(np.random.uniform(1.0, 5.0, len(df)), 1)
        
        # Add complications
        complications = ['None', 'Infection', 'Bleeding', 'Pneumonia', 'UTI', 'DVT']
        df['Complications'] = np.random.choice(complications, len(df), p=[0.7, 0.1, 0.05, 0.05, 0.05, 0.05])
        
        # Add vital signs
        df['Systolic BP'] = np.random.randint(90, 180, len(df))
        df['Diastolic BP'] = np.random.randint(60, 110, len(df))
        df['Heart Rate'] = np.random.randint(60, 120, len(df))
        df['Temperature'] = np.round(np.random.uniform(36.0, 39.0, len(df)), 1)
        df['Oxygen Saturation'] = np.random.randint(90, 100, len(df))
        
        # Add lab results
        df['Glucose'] = np.random.randint(70, 200, len(df))
        df['Creatinine'] = np.round(np.random.uniform(0.5, 2.0, len(df)), 2)
        df['Hemoglobin'] = np.round(np.random.uniform(10.0, 16.0, len(df)), 1)
        
        # Add procedure information
        procedures = ['None', 'Surgery', 'Endoscopy', 'Catheterization', 'Biopsy', 'Imaging']
        df['Procedures'] = np.random.choice(procedures, len(df), p=[0.4, 0.2, 0.15, 0.1, 0.1, 0.05])
        
        # Add cost breakdown
        df['Room Cost'] = np.random.randint(500, 2000, len(df))
        df['Medication Cost'] = np.random.randint(50, 500, len(df))
        df['Lab Cost'] = np.random.randint(100, 800, len(df))
        df['Procedure Cost'] = np.random.randint(0, 5000, len(df))
        
        # Calculate total cost
        df['Total Cost'] = df['Room Cost'] + df['Medication Cost'] + df['Lab Cost'] + df['Procedure Cost']
        
        # Add insurance coverage percentage
        df['Insurance Coverage'] = np.round(np.random.uniform(0.6, 0.95, len(df)), 2)
        
        # Calculate patient responsibility
        df['Patient Responsibility'] = np.round(df['Total Cost'] * (1 - df['Insurance Coverage']), 2)
        
        print(f"Enriched dataset: {len(df)} records")
        print(f"New columns: {list(df.columns)}")
        
        # Save enriched dataset
        enriched_path = 'healthcare_dataset_enriched.csv'
        df.to_csv(enriched_path, index=False)
        print(f"Enriched dataset saved to: {enriched_path}")
        
        return df
    
    def create_additional_datasets(self):
        """Create additional healthcare datasets"""
        print("\nCreating additional datasets...")
        
        # 1. Physician Performance Dataset
        print("Creating physician performance dataset...")
        physician_data = []
        for physician in self.physicians:
            for month in range(1, 13):
                physician_data.append({
                    'physician_id': f"PHY{self.physicians.index(physician):03d}",
                    'physician_name': physician,
                    'month': month,
                    'year': 2024,
                    'total_patients': np.random.randint(10, 50),
                    'avg_length_of_stay': round(np.random.uniform(2.0, 8.0), 1),
                    'avg_satisfaction_score': round(np.random.uniform(3.5, 5.0), 1),
                    'complication_rate': round(np.random.uniform(0.05, 0.20), 3),
                    'readmission_rate': round(np.random.uniform(0.10, 0.25), 3),
                    'avg_revenue': np.random.randint(5000, 25000)
                })
        
        physician_df = pd.DataFrame(physician_data)
        physician_df.to_csv('physician_performance.csv', index=False)
        print(f"Physician performance dataset: {len(physician_df)} records")
        
        # 2. Department Metrics Dataset
        print("Creating department metrics dataset...")
        department_data = []
        for department in self.departments:
            for month in range(1, 13):
                department_data.append({
                    'department_id': f"DEPT{self.departments.index(department):03d}",
                    'department_name': department,
                    'month': month,
                    'year': 2024,
                    'total_admissions': np.random.randint(50, 200),
                    'avg_length_of_stay': round(np.random.uniform(2.0, 10.0), 1),
                    'avg_cost': np.random.randint(3000, 15000),
                    'total_revenue': np.random.randint(200000, 1000000),
                    'occupancy_rate': round(np.random.uniform(0.6, 0.95), 2),
                    'nurse_patient_ratio': round(np.random.uniform(1.0, 3.0), 1)
                })
        
        department_df = pd.DataFrame(department_data)
        department_df.to_csv('department_metrics.csv', index=False)
        print(f"Department metrics dataset: {len(department_df)} records")
        
        # 3. Quality Metrics Dataset
        print("Creating quality metrics dataset...")
        quality_data = []
        for month in range(1, 13):
            quality_data.append({
                'month': month,
                'year': 2024,
                'hospital_acquired_infections': np.random.randint(5, 25),
                'pressure_ulcers': np.random.randint(2, 15),
                'falls': np.random.randint(10, 40),
                'medication_errors': np.random.randint(20, 80),
                'patient_satisfaction_avg': round(np.random.uniform(3.8, 4.8), 1),
                'readmission_rate': round(np.random.uniform(0.12, 0.22), 3),
                'mortality_rate': round(np.random.uniform(0.02, 0.08), 3),
                'avg_length_of_stay': round(np.random.uniform(4.0, 7.0), 1)
            })
        
        quality_df = pd.DataFrame(quality_data)
        quality_df.to_csv('quality_metrics.csv', index=False)
        print(f"Quality metrics dataset: {len(quality_df)} records")
        
        # 4. Financial Performance Dataset
        print("Creating financial performance dataset...")
        financial_data = []
        for month in range(1, 13):
            financial_data.append({
                'month': month,
                'year': 2024,
                'total_revenue': np.random.randint(5000000, 15000000),
                'total_expenses': np.random.randint(4000000, 12000000),
                'net_income': np.random.randint(500000, 3000000),
                'operating_margin': round(np.random.uniform(0.05, 0.20), 3),
                'bad_debt': np.random.randint(100000, 500000),
                'charity_care': np.random.randint(50000, 200000),
                'insurance_contractual': np.random.randint(200000, 800000),
                'cash_on_hand': np.random.randint(1000000, 5000000)
            })
        
        financial_df = pd.DataFrame(financial_data)
        financial_df.to_csv('financial_performance.csv', index=False)
        print(f"Financial performance dataset: {len(financial_df)} records")
        
        # 5. Patient Demographics Dataset
        print("Creating patient demographics dataset...")
        demographics_data = []
        age_groups = ['0-17', '18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
        
        for age_group in age_groups:
            for gender in ['M', 'F']:
                for insurance in self.insurance_providers:
                    demographics_data.append({
                        'age_group': age_group,
                        'gender': gender,
                        'insurance_type': insurance,
                        'patient_count': np.random.randint(50, 300),
                        'avg_length_of_stay': round(np.random.uniform(2.0, 8.0), 1),
                        'avg_cost': np.random.randint(3000, 12000),
                        'readmission_rate': round(np.random.uniform(0.10, 0.25), 3)
                    })
        
        demographics_df = pd.DataFrame(demographics_data)
        demographics_df.to_csv('patient_demographics.csv', index=False)
        print(f"Patient demographics dataset: {len(demographics_df)} records")
        
        return {
            'physician_performance': physician_df,
            'department_metrics': department_df,
            'quality_metrics': quality_df,
            'financial_performance': financial_df,
            'patient_demographics': demographics_df
        }
    
    def create_api_endpoints_data(self):
        """Create sample data for API endpoints"""
        print("\nCreating API endpoints data...")
        
        # Create a JSON file with sample API responses
        api_data = {
            'patients': {
                'endpoint': '/api/patients',
                'method': 'GET',
                'description': 'Get patient information',
                'sample_response': {
                    'patient_id': 'P001',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'age': 45,
                    'gender': 'M',
                    'insurance_type': 'Blue Cross Blue Shield'
                }
            },
            'admissions': {
                'endpoint': '/api/admissions',
                'method': 'GET',
                'description': 'Get admission information',
                'sample_response': {
                    'admission_id': 'A001',
                    'patient_name': 'John Doe',
                    'admission_date': '2024-01-15',
                    'discharge_date': '2024-01-18',
                    'admission_type': 'Emergency',
                    'department': 'Emergency Medicine'
                }
            },
            'metrics': {
                'endpoint': '/api/metrics',
                'method': 'GET',
                'description': 'Get key performance metrics',
                'sample_response': {
                    'patient_count': 9378,
                    'admission_count': 10000,
                    'total_revenue': 15000000,
                    'avg_length_of_stay': 4.2
                }
            },
            'analytics': {
                'endpoint': '/api/analytics',
                'method': 'GET',
                'description': 'Get analytics data',
                'sample_response': {
                    'monthly_admissions': [120, 135, 142, 128, 156, 143],
                    'top_diagnoses': ['Hypertension', 'Diabetes', 'Pneumonia'],
                    'department_performance': {
                        'Emergency Medicine': 2500,
                        'Cardiology': 1800,
                        'Orthopedics': 1200
                    }
                }
            }
        }
        
        with open('api_endpoints.json', 'w') as f:
            json.dump(api_data, f, indent=2)
        
        print("API endpoints data saved to: api_endpoints.json")
        return api_data
    
    def update_database_schema(self):
        """Update database schema with new tables"""
        print("\nUpdating database schema...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create additional tables
        additional_tables = [
            """
            CREATE TABLE IF NOT EXISTS physician_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                physician_id TEXT,
                physician_name TEXT,
                month INTEGER,
                year INTEGER,
                total_patients INTEGER,
                avg_length_of_stay REAL,
                avg_satisfaction_score REAL,
                complication_rate REAL,
                readmission_rate REAL,
                avg_revenue INTEGER,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS department_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_id TEXT,
                department_name TEXT,
                month INTEGER,
                year INTEGER,
                total_admissions INTEGER,
                avg_length_of_stay REAL,
                avg_cost INTEGER,
                total_revenue INTEGER,
                occupancy_rate REAL,
                nurse_patient_ratio REAL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS quality_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month INTEGER,
                year INTEGER,
                hospital_acquired_infections INTEGER,
                pressure_ulcers INTEGER,
                falls INTEGER,
                medication_errors INTEGER,
                patient_satisfaction_avg REAL,
                readmission_rate REAL,
                mortality_rate REAL,
                avg_length_of_stay REAL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS financial_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month INTEGER,
                year INTEGER,
                total_revenue INTEGER,
                total_expenses INTEGER,
                net_income INTEGER,
                operating_margin REAL,
                bad_debt INTEGER,
                charity_care INTEGER,
                insurance_contractual INTEGER,
                cash_on_hand INTEGER,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        for table_sql in additional_tables:
            cursor.execute(table_sql)
        
        conn.commit()
        conn.close()
        print("Database schema updated with additional tables")
    
    def load_additional_data_to_database(self, datasets):
        """Load additional datasets to database"""
        print("\nLoading additional data to database...")
        
        conn = sqlite3.connect(self.db_path)
        
        # Load physician performance
        datasets['physician_performance'].to_sql('physician_performance', conn, if_exists='replace', index=False)
        print(f"Loaded {len(datasets['physician_performance'])} physician performance records")
        
        # Load department metrics
        datasets['department_metrics'].to_sql('department_metrics', conn, if_exists='replace', index=False)
        print(f"Loaded {len(datasets['department_metrics'])} department metrics records")
        
        # Load quality metrics
        datasets['quality_metrics'].to_sql('quality_metrics', conn, if_exists='replace', index=False)
        print(f"Loaded {len(datasets['quality_metrics'])} quality metrics records")
        
        # Load financial performance
        datasets['financial_performance'].to_sql('financial_performance', conn, if_exists='replace', index=False)
        print(f"Loaded {len(datasets['financial_performance'])} financial performance records")
        
        conn.close()
        print("Additional data loaded to database")

def main():
    """Main function"""
    print("=== Healthcare Data Enrichment ===")
    
    # Initialize enrichment
    enrichment = HealthcareDataEnrichment()
    
    # Enrich main dataset
    enriched_df = enrichment.enrich_healthcare_data()
    
    # Create additional datasets
    additional_datasets = enrichment.create_additional_datasets()
    
    # Create API endpoints data
    api_data = enrichment.create_api_endpoints_data()
    
    # Update database schema
    enrichment.update_database_schema()
    
    # Load additional data to database
    enrichment.load_additional_data_to_database(additional_datasets)
    
    print("\n=== Data Enrichment Complete ===")
    print("Files created:")
    print("- healthcare_dataset_enriched.csv (Enhanced main dataset)")
    print("- physician_performance.csv (Physician metrics)")
    print("- department_metrics.csv (Department performance)")
    print("- quality_metrics.csv (Quality indicators)")
    print("- financial_performance.csv (Financial data)")
    print("- patient_demographics.csv (Demographic analysis)")
    print("- api_endpoints.json (API documentation)")
    print("\nDatabase updated with additional tables and data")

if __name__ == "__main__":
    main()
