"""
Healthcare Predictive Analytics - Random Forest vs XGBoost
Predicts patient readmission risk based on demographics and clinical data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc, roc_auc_score
)
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class HealthcarePredictiveModel:
    """
    Healthcare ML Pipeline for Readmission Prediction
    """
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.rf_model = None
        self.xgb_model = None
        self.label_encoders = {}
        
    def load_and_prepare_data(self):
        """Load and prepare the healthcare dataset"""
        print("=" * 70)
        print("STEP 1: LOADING AND PREPARING DATA")
        print("=" * 70)
        
        # Load data
        self.df = pd.read_csv(self.data_path)
        print(f"\n✅ Loaded dataset with {len(self.df)} records")
        print(f"📊 Features: {list(self.df.columns)}")
        
        # Display basic info
        print("\n📈 Dataset Info:")
        print(self.df.info())
        
        print("\n📊 Statistical Summary:")
        print(self.df.describe())
        
        # Check for missing values
        print("\n🔍 Missing Values:")
        print(self.df.isnull().sum())
        
        return self.df
    
    def create_target_variable(self, threshold=0.20):
        """
        Create binary target variable for readmission risk
        High risk: readmission_rate > threshold
        Low risk: readmission_rate <= threshold
        """
        print("\n" + "=" * 70)
        print("STEP 2: CREATING TARGET VARIABLE")
        print("=" * 70)
        
        # Create binary target
        self.df['high_readmission_risk'] = (self.df['readmission_rate'] > threshold).astype(int)
        
        print(f"\n✅ Target Variable Created:")
        print(f"   Threshold: {threshold}")
        print(f"   High Risk (1): {self.df['high_readmission_risk'].sum()} patients")
        print(f"   Low Risk (0): {len(self.df) - self.df['high_readmission_risk'].sum()} patients")
        print(f"   Class Balance: {self.df['high_readmission_risk'].mean():.2%} high risk")
        
        return self.df
    
    def encode_features(self):
        """Encode categorical features"""
        print("\n" + "=" * 70)
        print("STEP 3: ENCODING CATEGORICAL FEATURES")
        print("=" * 70)
        
        categorical_cols = ['age_group', 'gender', 'insurance_type']
        
        for col in categorical_cols:
            le = LabelEncoder()
            self.df[f'{col}_encoded'] = le.fit_transform(self.df[col])
            self.label_encoders[col] = le
            print(f"\n✅ Encoded {col}:")
            print(f"   Unique values: {self.df[col].nunique()}")
            print(f"   Categories: {list(le.classes_)}")
        
        return self.df
    
    def prepare_features(self):
        """Prepare features for modeling"""
        print("\n" + "=" * 70)
        print("STEP 4: PREPARING FEATURES")
        print("=" * 70)
        
        # Select features
        feature_cols = [
            'age_group_encoded', 'gender_encoded', 'insurance_type_encoded',
            'patient_count', 'avg_length_of_stay', 'avg_cost'
        ]
        
        X = self.df[feature_cols]
        y = self.df['high_readmission_risk']
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )
        
        print(f"\n✅ Features prepared:")
        print(f"   Total features: {len(feature_cols)}")
        print(f"   Feature names: {feature_cols}")
        print(f"\n📊 Data Split:")
        print(f"   Training set: {len(self.X_train)} samples ({len(self.X_train)/len(X):.1%})")
        print(f"   Test set: {len(self.X_test)} samples ({len(self.X_test)/len(X):.1%})")
        print(f"\n   Training - High Risk: {self.y_train.sum()} ({self.y_train.mean():.2%})")
        print(f"   Test - High Risk: {self.y_test.sum()} ({self.y_test.mean():.2%})")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_random_forest(self):
        """Train Random Forest model"""
        print("\n" + "=" * 70)
        print("STEP 5: TRAINING RANDOM FOREST MODEL")
        print("=" * 70)
        
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=10,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1
        )
        
        print("\n🌲 Training Random Forest...")
        self.rf_model.fit(self.X_train, self.y_train)
        
        # Cross-validation
        cv_scores = cross_val_score(self.rf_model, self.X_train, self.y_train, cv=5)
        print(f"✅ Training Complete!")
        print(f"   Cross-validation scores: {cv_scores}")
        print(f"   Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        return self.rf_model
    
    def train_xgboost(self):
        """Train XGBoost model"""
        print("\n" + "=" * 70)
        print("STEP 6: TRAINING XGBOOST MODEL")
        print("=" * 70)
        
        self.xgb_model = XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric='logloss'
        )
        
        print("\n🚀 Training XGBoost...")
        self.xgb_model.fit(self.X_train, self.y_train)
        
        # Cross-validation
        cv_scores = cross_val_score(self.xgb_model, self.X_train, self.y_train, cv=5)
        print(f"✅ Training Complete!")
        print(f"   Cross-validation scores: {cv_scores}")
        print(f"   Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        return self.xgb_model
    
    def evaluate_model(self, model, model_name):
        """Evaluate model performance"""
        print(f"\n{'=' * 70}")
        print(f"EVALUATING {model_name.upper()}")
        print("=" * 70)
        
        # Predictions
        y_pred = model.predict(self.X_test)
        y_pred_proba = model.predict_proba(self.X_test)[:, 1]
        
        # Metrics
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred)
        roc_auc = roc_auc_score(self.y_test, y_pred_proba)
        
        print(f"\n📊 {model_name} Performance Metrics:")
        print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"   Precision: {precision:.4f} ({precision*100:.2f}%)")
        print(f"   Recall:    {recall:.4f} ({recall*100:.2f}%)")
        print(f"   F1-Score:  {f1:.4f}")
        print(f"   ROC-AUC:   {roc_auc:.4f}")
        
        print(f"\n📋 Classification Report:")
        print(classification_report(self.y_test, y_pred, target_names=['Low Risk', 'High Risk']))
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
    
    def get_feature_importance(self, model, model_name):
        """Get feature importance"""
        feature_names = [
            'Age Group', 'Gender', 'Insurance Type',
            'Patient Count', 'Length of Stay', 'Avg Cost'
        ]
        
        importance = model.feature_importances_
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        print(f"\n🎯 {model_name} - Top Feature Importances:")
        for idx, row in feature_importance.iterrows():
            print(f"   {row['feature']:20s}: {row['importance']:.4f} ({row['importance']*100:.2f}%)")
        
        return feature_importance
    
    def run_complete_pipeline(self):
        """Run the complete ML pipeline"""
        print("\n" + "=" * 70)
        print("🏥 HEALTHCARE READMISSION PREDICTION - ML PIPELINE")
        print("=" * 70)
        print("Models: Random Forest vs XGBoost")
        print("Task: Predict High Readmission Risk")
        print("=" * 70)
        
        # Load and prepare data
        self.load_and_prepare_data()
        self.create_target_variable(threshold=0.20)
        self.encode_features()
        self.prepare_features()
        
        # Train models
        self.train_random_forest()
        self.train_xgboost()
        
        # Evaluate models
        rf_results = self.evaluate_model(self.rf_model, "Random Forest")
        xgb_results = self.evaluate_model(self.xgb_model, "XGBoost")
        
        # Feature importance
        rf_importance = self.get_feature_importance(self.rf_model, "Random Forest")
        xgb_importance = self.get_feature_importance(self.xgb_model, "XGBoost")
        
        # Store results
        results = {
            'rf': rf_results,
            'xgb': xgb_results,
            'rf_importance': rf_importance,
            'xgb_importance': xgb_importance
        }
        
        return results

if __name__ == "__main__":
    # Initialize pipeline
    pipeline = HealthcarePredictiveModel('data/patient_demographics.csv')
    
    # Run complete pipeline
    results = pipeline.run_complete_pipeline()
    
    print("\n" + "=" * 70)
    print("✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nNext: Run visualization script to generate graphs")
