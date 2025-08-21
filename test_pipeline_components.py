#!/usr/bin/env python3
"""
Test script to verify pipeline components
"""

import pandas as pd
import sqlite3
from healthcare_pipeline import HealthcarePipeline, PipelineConfig, DataValidator, DataTransformer
from pipeline_scheduler import PipelineScheduler, PipelineMonitor

def test_pipeline_components():
    """Test all pipeline components"""
    
    print("=== Testing Healthcare Pipeline Components ===\n")
    
    # Test 1: Data Validation
    print("1. Testing Data Validation...")
    df = pd.read_csv('healthcare_dataset.csv')
    is_valid, errors = DataValidator.validate_patient_data(df)
    print(f"   Patient validation: {'PASS' if is_valid else 'FAIL'}")
    if errors:
        print(f"   Errors: {errors}")
    
    # Test 2: Data Transformation
    print("\n2. Testing Data Transformation...")
    df_clean = DataTransformer.clean_patient_data(df)
    df_clean = DataTransformer.clean_admission_data(df_clean)
    df_clean = DataTransformer.clean_financial_data(df_clean)
    print(f"   Transformation: PASS ({len(df_clean)} records)")
    
    # Test 3: Database Connection
    print("\n3. Testing Database Connection...")
    try:
        conn = sqlite3.connect('healthcare_analytics.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM admissions")
        admission_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM financial_data")
        financial_count = cursor.fetchone()[0]
        conn.close()
        print(f"   Database connection: PASS")
        print(f"   Patients: {patient_count}")
        print(f"   Admissions: {admission_count}")
        print(f"   Financial records: {financial_count}")
    except Exception as e:
        print(f"   Database connection: FAIL - {str(e)}")
    
    # Test 4: Pipeline Configuration
    print("\n4. Testing Pipeline Configuration...")
    config = PipelineConfig(
        source_type='csv',
        source_path='healthcare_dataset.csv',
        target_database='sqlite',
        target_connection='healthcare_analytics.db'
    )
    print(f"   Configuration: PASS")
    
    # Test 5: Scheduler
    print("\n5. Testing Scheduler...")
    try:
        scheduler = PipelineScheduler('pipeline_config.yaml')
        status = scheduler.get_pipeline_status()
        print(f"   Scheduler: PASS")
        print(f"   Total jobs: {status['total_jobs']}")
    except Exception as e:
        print(f"   Scheduler: FAIL - {str(e)}")
    
    # Test 6: Monitor
    print("\n6. Testing Monitor...")
    try:
        monitor = PipelineMonitor(scheduler)
        health_report = monitor.generate_health_report()
        print(f"   Monitor: PASS")
        print(f"   System health: {health_report['overall_health']}")
    except Exception as e:
        print(f"   Monitor: FAIL - {str(e)}")
    
    print("\n=== All Tests Completed ===")

if __name__ == "__main__":
    test_pipeline_components()
