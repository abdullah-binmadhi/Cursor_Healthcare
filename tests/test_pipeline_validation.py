#!/usr/bin/env python3
"""
Test script to check pipeline validation errors
"""

import pandas as pd
from healthcare_pipeline import DataValidator

def test_validation():
    """Test data validation"""
    
    # Load data
    print("Loading healthcare dataset...")
    df = pd.read_csv('healthcare_dataset.csv')
    print(f"Loaded {len(df)} records")
    print(f"Columns: {list(df.columns)}")
    
    # Test patient validation
    print("\n=== Testing Patient Data Validation ===")
    is_valid_patients, patient_errors = DataValidator.validate_patient_data(df)
    print(f"Patient validation passed: {is_valid_patients}")
    if patient_errors:
        print("Patient validation errors:")
        for error in patient_errors:
            print(f"  - {error}")
    
    # Test admission validation
    print("\n=== Testing Admission Data Validation ===")
    is_valid_admissions, admission_errors = DataValidator.validate_admission_data(df)
    print(f"Admission validation passed: {is_valid_admissions}")
    if admission_errors:
        print("Admission validation errors:")
        for error in admission_errors:
            print(f"  - {error}")
    
    # Test financial validation
    print("\n=== Testing Financial Data Validation ===")
    is_valid_financial, financial_errors = DataValidator.validate_financial_data(df)
    print(f"Financial validation passed: {is_valid_financial}")
    if financial_errors:
        print("Financial validation errors:")
        for error in financial_errors:
            print(f"  - {error}")
    
    # Show sample data
    print("\n=== Sample Data ===")
    print(df.head())
    
    # Check data types
    print("\n=== Data Types ===")
    print(df.dtypes)
    
    # Check for missing values
    print("\n=== Missing Values ===")
    print(df.isnull().sum())

if __name__ == "__main__":
    test_validation()
