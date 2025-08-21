#!/usr/bin/env python3
"""
Healthcare Data Pipeline
A comprehensive ETL pipeline for healthcare analytics with data validation, error handling, and monitoring
"""

import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine, text
import numpy as np
from datetime import datetime, timedelta
import logging
import json
import os
import sys
from pathlib import Path
import hashlib
from typing import Dict, List, Optional, Tuple
import schedule
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('healthcare_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PipelineConfig:
    """Configuration for the healthcare pipeline"""
    source_type: str = 'csv'  # csv, api, database
    source_path: str = 'healthcare_dataset.csv'
    target_database: str = 'sqlite'  # sqlite, postgresql
    target_connection: str = 'healthcare_analytics.db'
    batch_size: int = 1000
    validation_enabled: bool = True
    backup_enabled: bool = True
    monitoring_enabled: bool = True
    schedule_interval: str = 'daily'  # daily, hourly, weekly

class DataValidator:
    """Data validation and quality checks"""
    
    @staticmethod
    def validate_patient_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate patient data quality"""
        errors = []
        
        # Check required columns
        required_columns = ['Name', 'Age', 'Gender', 'Insurance Provider']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")
        
        # Validate age range
        if 'Age' in df.columns:
            invalid_ages = df[df['Age'] < 0]['Age'].count()
            if invalid_ages > 0:
                errors.append(f"Found {invalid_ages} records with negative age")
        
        # Validate gender values
        if 'Gender' in df.columns:
            valid_genders = ['Male', 'Female', 'M', 'F']
            invalid_genders = df[~df['Gender'].isin(valid_genders)]['Gender'].unique()
            if len(invalid_genders) > 0:
                errors.append(f"Invalid gender values: {invalid_genders}")
        
        # Check for duplicate patient names (only if strict mode is enabled)
        if 'Name' in df.columns:
            duplicates = df['Name'].duplicated().sum()
            if duplicates > 0:
                # In healthcare, patients can have multiple admissions, so duplicates are expected
                # Only warn if there are excessive duplicates (more than 50% of records)
                if duplicates > len(df) * 0.5:
                    errors.append(f"Found {duplicates} duplicate patient names (excessive)")
                else:
                    logger.info(f"Found {duplicates} duplicate patient names (expected in healthcare data)")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_admission_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate admission data quality"""
        errors = []
        
        # Check required columns
        required_columns = ['Date of Admission', 'Discharge Date', 'Admission Type']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")
        
        # Validate date ranges
        if 'Date of Admission' in df.columns and 'Discharge Date' in df.columns:
            df['admission_date'] = pd.to_datetime(df['Date of Admission'], errors='coerce')
            df['discharge_date'] = pd.to_datetime(df['Discharge Date'], errors='coerce')
            
            # Check for future dates
            future_admissions = df[df['admission_date'] > datetime.now()]['admission_date'].count()
            if future_admissions > 0:
                errors.append(f"Found {future_admissions} admissions with future dates")
            
            # Check for discharge before admission
            invalid_discharge = df[df['discharge_date'] < df['admission_date']].shape[0]
            if invalid_discharge > 0:
                errors.append(f"Found {invalid_discharge} records with discharge before admission")
        
        # Validate admission types
        if 'Admission Type' in df.columns:
            valid_types = ['Emergency', 'Elective', 'Urgent', 'Transfer']
            invalid_types = df[~df['Admission Type'].isin(valid_types)]['Admission Type'].unique()
            if len(invalid_types) > 0:
                errors.append(f"Invalid admission types: {invalid_types}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_financial_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate financial data quality"""
        errors = []
        
        # Check for negative amounts
        if 'Billing Amount' in df.columns:
            negative_amounts = df[df['Billing Amount'] < 0]['Billing Amount'].count()
            if negative_amounts > 0:
                errors.append(f"Found {negative_amounts} records with negative billing amounts")
        
        # Check for extremely high amounts (outliers)
        if 'Billing Amount' in df.columns:
            q99 = df['Billing Amount'].quantile(0.99)
            outliers = df[df['Billing Amount'] > q99 * 10]['Billing Amount'].count()
            if outliers > 0:
                errors.append(f"Found {outliers} records with extremely high billing amounts")
        
        return len(errors) == 0, errors

class DataTransformer:
    """Data transformation and cleaning"""
    
    @staticmethod
    def clean_patient_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize patient data"""
        df_clean = df.copy()
        
        # Clean column names
        df_clean.columns = df_clean.columns.str.strip()
        
        # Extract first and last name
        if 'Name' in df_clean.columns:
            name_parts = df_clean['Name'].str.split(' ', n=1, expand=True)
            df_clean['first_name'] = name_parts[0]
            df_clean['last_name'] = name_parts[1].fillna('')
        
        # Standardize gender
        if 'Gender' in df_clean.columns:
            gender_mapping = {
                'Male': 'M', 'Female': 'F', 'MALE': 'M', 'FEMALE': 'F'
            }
            df_clean['Gender'] = df_clean['Gender'].map(gender_mapping).fillna('Unknown')
        
        # Create patient IDs
        df_clean['patient_id'] = df_clean['Name'].apply(
            lambda x: hashlib.md5(x.encode()).hexdigest()[:12]
        )
        
        # Estimate date of birth from age
        if 'Age' in df_clean.columns:
            current_year = datetime.now().year
            df_clean['date_of_birth'] = pd.to_datetime(
                (current_year - df_clean['Age']).astype(str) + '-01-01',
                errors='coerce'
            )
        
        return df_clean
    
    @staticmethod
    def clean_admission_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize admission data"""
        df_clean = df.copy()
        
        # Convert dates
        date_columns = ['Date of Admission', 'Discharge Date']
        for col in date_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
        
        # Calculate length of stay
        if 'Date of Admission' in df_clean.columns and 'Discharge Date' in df_clean.columns:
            df_clean['length_of_stay'] = (
                df_clean['Discharge Date'] - df_clean['Date of Admission']
            ).dt.days
        
        # Standardize admission types
        if 'Admission Type' in df_clean.columns:
            df_clean['Admission Type'] = df_clean['Admission Type'].str.title()
        
        # Clean room numbers
        if 'Room Number' in df_clean.columns:
            df_clean['Room Number'] = df_clean['Room Number'].astype(str).str.strip()
        
        return df_clean
    
    @staticmethod
    def clean_financial_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize financial data"""
        df_clean = df.copy()
        
        # Convert billing amount to numeric
        if 'Billing Amount' in df_clean.columns:
            df_clean['Billing Amount'] = pd.to_numeric(df_clean['Billing Amount'], errors='coerce')
        
        # Remove outliers (values beyond 3 standard deviations)
        if 'Billing Amount' in df_clean.columns:
            mean_amount = df_clean['Billing Amount'].mean()
            std_amount = df_clean['Billing Amount'].std()
            lower_bound = mean_amount - 3 * std_amount
            upper_bound = mean_amount + 3 * std_amount
            
            df_clean = df_clean[
                (df_clean['Billing Amount'] >= lower_bound) & 
                (df_clean['Billing Amount'] <= upper_bound)
            ]
        
        return df_clean

class DataLoader:
    """Data loading and database operations"""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.engine = self._create_engine()
    
    def _create_engine(self):
        """Create database engine based on configuration"""
        if self.config.target_database == 'sqlite':
            return create_engine(f'sqlite:///{self.config.target_connection}')
        elif self.config.target_database == 'postgresql':
            return create_engine(self.config.target_connection)
        else:
            raise ValueError(f"Unsupported database type: {self.config.target_database}")
    
    def load_patients(self, df: pd.DataFrame) -> bool:
        """Load patient data into database"""
        try:
            # Create unique patients by patient_id
            unique_patients = df.drop_duplicates(subset=['patient_id'])
            
            patients_data = []
            for _, row in unique_patients.iterrows():
                patients_data.append({
                    'patient_id': row['patient_id'],
                    'first_name': row.get('first_name', ''),
                    'last_name': row.get('last_name', ''),
                    'date_of_birth': row.get('date_of_birth'),
                    'gender': row['Gender'],
                    'insurance_type': row['Insurance Provider'],
                    'created_date': datetime.now(),
                    'updated_date': datetime.now()
                })
            
            patients_df = pd.DataFrame(patients_data)
            patients_df.to_sql('patients', self.engine, if_exists='append', index=False)
            logger.info(f"Loaded {len(patients_df)} unique patient records")
            return True
            
        except Exception as e:
            logger.error(f"Error loading patients: {str(e)}")
            return False
    
    def load_admissions(self, df: pd.DataFrame) -> bool:
        """Load admission data into database"""
        try:
            admissions_data = []
            for _, row in df.iterrows():
                admissions_data.append({
                    'patient_id': row['patient_id'],
                    'admission_date': row['Date of Admission'],
                    'discharge_date': row['Discharge Date'],
                    'admission_type': row['Admission Type'],
                    'department': 'General',
                    'attending_physician': row['Doctor'],
                    'room_number': row['Room Number'],
                    'created_date': datetime.now()
                })
            
            admissions_df = pd.DataFrame(admissions_data)
            admissions_df.to_sql('admissions', self.engine, if_exists='append', index=False)
            logger.info(f"Loaded {len(admissions_df)} admission records")
            return True
            
        except Exception as e:
            logger.error(f"Error loading admissions: {str(e)}")
            return False
    
    def load_financial_data(self, df: pd.DataFrame) -> bool:
        """Load financial data into database"""
        try:
            financial_data = []
            for idx, row in df.iterrows():
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
            
            financial_df = pd.DataFrame(financial_data)
            financial_df.to_sql('financial_data', self.engine, if_exists='append', index=False)
            logger.info(f"Loaded {len(financial_df)} financial records")
            return True
            
        except Exception as e:
            logger.error(f"Error loading financial data: {str(e)}")
            return False

class PipelineMonitor:
    """Pipeline monitoring and metrics"""
    
    def __init__(self):
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'records_processed': 0,
            'records_failed': 0,
            'validation_errors': [],
            'processing_time': 0
        }
    
    def start_pipeline(self):
        """Start pipeline monitoring"""
        self.metrics['start_time'] = datetime.now()
        logger.info("Pipeline started")
    
    def end_pipeline(self):
        """End pipeline monitoring"""
        self.metrics['end_time'] = datetime.now()
        self.metrics['processing_time'] = (
            self.metrics['end_time'] - self.metrics['start_time']
        ).total_seconds()
        logger.info(f"Pipeline completed in {self.metrics['processing_time']:.2f} seconds")
    
    def add_validation_error(self, error: str):
        """Add validation error"""
        self.metrics['validation_errors'].append(error)
        self.metrics['records_failed'] += 1
    
    def increment_processed(self, count: int = 1):
        """Increment processed records count"""
        self.metrics['records_processed'] += count
    
    def get_summary(self) -> Dict:
        """Get pipeline summary"""
        return {
            'status': 'completed' if self.metrics['end_time'] else 'running',
            'processing_time_seconds': self.metrics['processing_time'],
            'records_processed': self.metrics['records_processed'],
            'records_failed': self.metrics['records_failed'],
            'success_rate': (
                (self.metrics['records_processed'] - self.metrics['records_failed']) / 
                max(self.metrics['records_processed'], 1) * 100
            ),
            'validation_errors': len(self.metrics['validation_errors'])
        }
    
    def save_metrics(self, filename: str = 'pipeline_metrics.json'):
        """Save metrics to file"""
        with open(filename, 'w') as f:
            json.dump(self.metrics, f, default=str, indent=2)

class HealthcarePipeline:
    """Main healthcare data pipeline"""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.validator = DataValidator()
        self.transformer = DataTransformer()
        self.loader = DataLoader(config)
        self.monitor = PipelineMonitor()
        
    def extract_data(self) -> pd.DataFrame:
        """Extract data from source"""
        logger.info(f"Extracting data from {self.config.source_path}")
        
        if self.config.source_type == 'csv':
            df = pd.read_csv(self.config.source_path)
        elif self.config.source_type == 'api':
            # Implement API extraction here
            raise NotImplementedError("API extraction not implemented yet")
        else:
            raise ValueError(f"Unsupported source type: {self.config.source_type}")
        
        logger.info(f"Extracted {len(df)} records")
        return df
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate data quality"""
        logger.info("Validating data quality")
        
        # Validate patient data
        is_valid_patients, patient_errors = self.validator.validate_patient_data(df)
        for error in patient_errors:
            self.monitor.add_validation_error(f"Patient data: {error}")
        
        # Validate admission data
        is_valid_admissions, admission_errors = self.validator.validate_admission_data(df)
        for error in admission_errors:
            self.monitor.add_validation_error(f"Admission data: {error}")
        
        # Validate financial data
        is_valid_financial, financial_errors = self.validator.validate_financial_data(df)
        for error in financial_errors:
            self.monitor.add_validation_error(f"Financial data: {error}")
        
        is_valid = is_valid_patients and is_valid_admissions and is_valid_financial
        
        if is_valid:
            logger.info("Data validation passed")
        else:
            logger.warning(f"Data validation failed with {len(patient_errors + admission_errors + financial_errors)} errors")
        
        return is_valid
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform and clean data"""
        logger.info("Transforming data")
        
        # Clean patient data
        df_clean = self.transformer.clean_patient_data(df)
        
        # Clean admission data
        df_clean = self.transformer.clean_admission_data(df_clean)
        
        # Clean financial data
        df_clean = self.transformer.clean_financial_data(df_clean)
        
        logger.info(f"Transformed {len(df_clean)} records")
        return df_clean
    
    def load_data(self, df: pd.DataFrame) -> bool:
        """Load data into target database"""
        logger.info("Loading data into database")
        
        success = True
        
        # Load patients
        if not self.loader.load_patients(df):
            success = False
        
        # Load admissions
        if not self.loader.load_admissions(df):
            success = False
        
        # Load financial data
        if not self.loader.load_financial_data(df):
            success = False
        
        if success:
            logger.info("Data loading completed successfully")
        else:
            logger.error("Data loading failed")
        
        return success
    
    def create_backup(self):
        """Create database backup"""
        if not self.config.backup_enabled:
            return
        
        try:
            backup_dir = Path('backups')
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = backup_dir / f'healthcare_backup_{timestamp}.db'
            
            if self.config.target_database == 'sqlite':
                import shutil
                shutil.copy2(self.config.target_connection, backup_file)
                logger.info(f"Backup created: {backup_file}")
            
        except Exception as e:
            logger.error(f"Backup failed: {str(e)}")
    
    def run_pipeline(self) -> bool:
        """Run the complete pipeline"""
        self.monitor.start_pipeline()
        
        try:
            # Extract
            df = self.extract_data()
            self.monitor.increment_processed(len(df))
            
            # Validate
            if self.config.validation_enabled:
                if not self.validate_data(df):
                    logger.error("Data validation failed")
                    return False
            
            # Transform
            df_clean = self.transform_data(df)
            
            # Load
            if not self.load_data(df_clean):
                logger.error("Data loading failed")
                return False
            
            # Create backup
            self.create_backup()
            
            self.monitor.end_pipeline()
            
            # Save metrics
            if self.config.monitoring_enabled:
                self.monitor.save_metrics()
            
            # Log summary
            summary = self.monitor.get_summary()
            logger.info(f"Pipeline summary: {summary}")
            
            return True
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            self.monitor.end_pipeline()
            return False

def run_scheduled_pipeline(config: PipelineConfig):
    """Run pipeline on schedule"""
    pipeline = HealthcarePipeline(config)
    pipeline.run_pipeline()

def main():
    """Main function"""
    # Configuration
    config = PipelineConfig(
        source_type='csv',
        source_path='healthcare_dataset.csv',
        target_database='sqlite',
        target_connection='healthcare_analytics.db',
        batch_size=1000,
        validation_enabled=True,
        backup_enabled=True,
        monitoring_enabled=True,
        schedule_interval='daily'
    )
    
    # Run pipeline
    pipeline = HealthcarePipeline(config)
    success = pipeline.run_pipeline()
    
    if success:
        print("✅ Healthcare pipeline completed successfully!")
    else:
        print("❌ Healthcare pipeline failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
