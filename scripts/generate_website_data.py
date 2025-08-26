"""
Healthcare Data Extractor for Website
Generates CSV files with sample data for the healthcare website
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import csv
import os

def generate_sample_data():
    """Generate sample healthcare data for the website"""
    
    # Set random seed for reproducible data
    random.seed(42)
    np.random.seed(42)
    
    # Define sample data lists
    specialties = ['Cardiology', 'Emergency Medicine', 'Surgery', 'Orthopedics', 
                  'Neurology', 'Pediatrics', 'Oncology']
    
    departments = ['Cardiology', 'Emergency', 'Surgery', 'Orthopedics', 
                  'Neurology', 'Pediatrics', 'Oncology']
    
    hospitals = ['City General Hospital', 'St. Mary\'s Medical Center', 
                'University Health System', 'Memorial Hospital', 
                'Regional Medical Center', 'Community Health Hospital',
                'Metropolitan Medical Center', 'Riverside Hospital']
    
    insurance_types = ['Medicare', 'Medicaid', 'Private Insurance', 'Self-Pay', 'Commercial']
    
    procedures = ['Consultation', 'Diagnostic Test', 'Minor Surgery', 
                 'Major Surgery', 'Emergency Visit', 'Follow-up Visit']
    
    # Generate physician data
    physician_data = []
    for i in range(150):
        specialty = random.choice(specialties)
        department = specialty if specialty != 'Emergency Medicine' else 'Emergency'
        
        physician = {
            'physician_id': f'DOC{i+1:03d}',
            'first_name': random.choice(['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa']),
            'last_name': random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']),
            'specialty': specialty,
            'department': department,
            'hospital': random.choice(hospitals),
            'years_experience': random.randint(5, 30),
            'patient_satisfaction': round(random.uniform(3.5, 5.0), 1),
            'complication_rate': round(random.uniform(0.5, 5.0), 2),
            'average_wait_time': random.randint(15, 120),
            'availability_status': random.choice(['Available', 'Limited', 'Unavailable']),
            'total_patients': random.randint(500, 2000),
            'success_rate': round(random.uniform(85, 99), 1)
        }
        physician_data.append(physician)
    
    # Generate department metrics
    department_data = []
    for dept in departments:
        dept_metrics = {
            'department_name': dept,
            'total_patients': random.randint(1000, 5000),
            'average_length_stay': round(random.uniform(2.5, 8.5), 1),
            'readmission_rate': round(random.uniform(5, 15), 2),
            'patient_satisfaction': round(random.uniform(4.0, 4.8), 1),
            'average_cost': random.randint(2000, 15000),
            'bed_capacity': random.randint(50, 200),
            'current_occupancy': round(random.uniform(0.6, 0.95), 2),
            'staff_count': random.randint(20, 100)
        }
        department_data.append(dept_metrics)
    
    # Generate financial performance data
    financial_data = []
    for dept in departments:
        for insurance in insurance_types:
            for procedure in procedures:
                financial = {
                    'department': dept,
                    'insurance_type': insurance,
                    'procedure_type': procedure,
                    'base_cost': random.randint(500, 8000),
                    'insurance_coverage_pct': round(random.uniform(0.6, 0.9), 2),
                    'average_patient_cost': 0,  # Will calculate
                    'volume': random.randint(10, 200),
                    'total_revenue': 0,  # Will calculate
                    'length_of_stay_days': round(random.uniform(1, 7), 1)
                }
                
                # Calculate derived values
                coverage_amount = financial['base_cost'] * financial['insurance_coverage_pct']
                financial['average_patient_cost'] = max(0, financial['base_cost'] - coverage_amount)
                financial['total_revenue'] = financial['base_cost'] * financial['volume']
                
                financial_data.append(financial)
    
    # Generate patient demographics
    demographics_data = []
    age_groups = ['0-18', '19-30', '31-50', '51-65', '65+']
    genders = ['Male', 'Female']
    
    for age_group in age_groups:
        for gender in genders:
            for insurance in insurance_types:
                demo = {
                    'age_group': age_group,
                    'gender': gender,
                    'insurance_type': insurance,
                    'patient_count': random.randint(50, 500),
                    'avg_annual_cost': random.randint(2000, 12000),
                    'common_conditions': random.choice(['Diabetes', 'Hypertension', 'Heart Disease', 'Cancer', 'Injury']),
                    'readmission_rate': round(random.uniform(5, 20), 1),
                    'satisfaction_score': round(random.uniform(3.5, 4.8), 1)
                }
                demographics_data.append(demo)
    
    # Generate quality metrics
    quality_data = []
    metrics = ['Infection Rate', 'Readmission Rate', 'Mortality Rate', 'Patient Satisfaction', 
              'Length of Stay', 'Complication Rate']
    
    for dept in departments:
        for metric in metrics:
            quality = {
                'department': dept,
                'metric_name': metric,
                'current_value': round(random.uniform(1, 20), 2),
                'target_value': round(random.uniform(1, 15), 2),
                'benchmark_value': round(random.uniform(5, 25), 2),
                'trend': random.choice(['Improving', 'Stable', 'Declining']),
                'measurement_period': 'Monthly',
                'last_updated': datetime.now().strftime('%Y-%m-%d')
            }
            quality_data.append(quality)
    
    return physician_data, department_data, financial_data, demographics_data, quality_data

def save_csv_files(physician_data, department_data, financial_data, demographics_data, quality_data):
    """Save data to CSV files in the website data directory"""
    
    # Create data directory if it doesn't exist
    data_dir = 'healthcare-website/data'
    os.makedirs(data_dir, exist_ok=True)
    
    # Save physician performance data
    physician_df = pd.DataFrame(physician_data)
    physician_df.to_csv(f'{data_dir}/physician_performance.csv', index=False)
    print(f"Created {data_dir}/physician_performance.csv with {len(physician_data)} records")
    
    # Save department metrics
    department_df = pd.DataFrame(department_data)
    department_df.to_csv(f'{data_dir}/department_metrics.csv', index=False)
    print(f"Created {data_dir}/department_metrics.csv with {len(department_data)} records")
    
    # Save financial performance
    financial_df = pd.DataFrame(financial_data)
    financial_df.to_csv(f'{data_dir}/financial_performance.csv', index=False)
    print(f"Created {data_dir}/financial_performance.csv with {len(financial_data)} records")
    
    # Save patient demographics
    demographics_df = pd.DataFrame(demographics_data)
    demographics_df.to_csv(f'{data_dir}/patient_demographics.csv', index=False)
    print(f"Created {data_dir}/patient_demographics.csv with {len(demographics_data)} records")
    
    # Save quality metrics
    quality_df = pd.DataFrame(quality_data)
    quality_df.to_csv(f'{data_dir}/quality_metrics.csv', index=False)
    print(f"Created {data_dir}/quality_metrics.csv with {len(quality_data)} records")

def main():
    """Main function to generate and save healthcare data"""
    print("Generating sample healthcare data for website...")
    
    # Generate all data
    physician_data, department_data, financial_data, demographics_data, quality_data = generate_sample_data()
    
    # Save to CSV files
    save_csv_files(physician_data, department_data, financial_data, demographics_data, quality_data)
    
    print("✅ All CSV files created successfully!")
    print("\nFiles created:")
    print("- physician_performance.csv: Doctor profiles with ratings and metrics (150 doctors)")
    print("- department_metrics.csv: Department performance and capacity data")
    print("- financial_performance.csv: Cost estimates by department, insurance, and procedure")
    print("- patient_demographics.csv: Patient population statistics")
    print("- quality_metrics.csv: Healthcare quality indicators")

if __name__ == "__main__":
    main()