"""
Healthcare ML Visualization - Complete Graph Generator
Creates all 14 visualizations for comprehensive analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from healthcare_ml_pipeline import HealthcarePredictiveModel

# Professional healthcare color palette
COLORS = {
    'primary': '#1a5f7a',
    'secondary': '#2ecc71',
    'accent': '#3498db',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'dark': '#2c3e50',
    'light': '#ecf0f1'
}

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'figure.figsize': (12, 8),
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.dpi': 150
})

class ComprehensiveVisualizer:
    def __init__(self, pipeline=None, results=None):
        self.pipeline = pipeline
        self.results = results
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'graphs')
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load datasets
        self.patient_df = pd.read_csv(os.path.join(self.data_dir, 'patient_demographics.csv'))
        self.physician_df = pd.read_csv(os.path.join(self.data_dir, 'physician_performance.csv'))
        self.dept_df = pd.read_csv(os.path.join(self.data_dir, 'department_metrics.csv'))
        self.financial_df = pd.read_csv(os.path.join(self.data_dir, 'financial_performance.csv'))
        self.registry_df = pd.read_csv(os.path.join(self.data_dir, 'physician_registry.csv'))

    # ===== EXISTING GRAPHS (1-7) - Enhanced =====
    
    def plot_1_model_comparison(self):
        """Graph 1: Model Comparison Metrics"""
        print("📊 Generating Graph 1: Model Comparison...")
        
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
        rf = [self.results['rf'][m.lower().replace('-', '_').replace(' ', '_')] for m in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']]
        xgb = [self.results['xgb'][m.lower().replace('-', '_').replace(' ', '_')] for m in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars1 = ax.bar(x - width/2, rf, width, label='Random Forest', color=COLORS['secondary'], edgecolor='black', linewidth=1.2)
        bars2 = ax.bar(x + width/2, xgb, width, label='XGBoost', color=COLORS['accent'], edgecolor='black', linewidth=1.2)
        
        ax.set_xlabel('Performance Metrics', fontweight='bold')
        ax.set_ylabel('Score', fontweight='bold')
        ax.set_title('Healthcare Readmission Prediction\nRandom Forest vs XGBoost Performance', fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, fontweight='bold')
        ax.legend(loc='upper right', framealpha=0.9)
        ax.set_ylim([0, 1.15])
        ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Baseline')
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.3f}', xy=(bar.get_x() + bar.get_width()/2, height),
                           xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/1_model_comparison_metrics.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 1_model_comparison_metrics.png")

    def plot_2_confusion_matrices(self):
        """Graph 2: Confusion Matrices"""
        print("📊 Generating Graph 2: Confusion Matrices...")
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        
        for idx, (name, y_pred, color) in enumerate([
            ('Random Forest', self.results['rf']['y_pred'], COLORS['secondary']),
            ('XGBoost', self.results['xgb']['y_pred'], COLORS['accent'])
        ]):
            cm = confusion_matrix(self.pipeline.y_test, y_pred)
            cm_pct = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
            
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       square=True, cbar_kws={'label': 'Count', 'shrink': 0.8},
                       xticklabels=['Low Risk', 'High Risk'],
                       yticklabels=['Low Risk', 'High Risk'],
                       annot_kws={'size': 14, 'weight': 'bold'})
            
            for i in range(2):
                for j in range(2):
                    axes[idx].text(j + 0.5, i + 0.75, f'({cm_pct[i,j]:.1f}%)',
                                  ha='center', va='center', fontsize=10, color='darkred', fontweight='bold')
            
            axes[idx].set_title(f'{name}\nConfusion Matrix', fontweight='bold', pad=15, fontsize=14)
            axes[idx].set_ylabel('Actual Label', fontweight='bold')
            axes[idx].set_xlabel('Predicted Label', fontweight='bold')
        
        plt.suptitle('Patient Readmission Risk - Classification Results', fontweight='bold', fontsize=16, y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/2_confusion_matrices.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 2_confusion_matrices.png")

    def plot_3_roc_curves(self):
        """Graph 3: ROC Curves"""
        print("📊 Generating Graph 3: ROC Curves...")
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        fpr_rf, tpr_rf, _ = roc_curve(self.pipeline.y_test, self.results['rf']['y_pred_proba'])
        fpr_xgb, tpr_xgb, _ = roc_curve(self.pipeline.y_test, self.results['xgb']['y_pred_proba'])
        
        ax.plot(fpr_rf, tpr_rf, color=COLORS['secondary'], lw=3, label=f'Random Forest (AUC = {auc(fpr_rf, tpr_rf):.3f})')
        ax.plot(fpr_xgb, tpr_xgb, color=COLORS['accent'], lw=3, label=f'XGBoost (AUC = {auc(fpr_xgb, tpr_xgb):.3f})')
        ax.plot([0, 1], [0, 1], 'r--', lw=2, label='Random Classifier (AUC = 0.500)')
        
        ax.fill_between(fpr_rf, tpr_rf, alpha=0.1, color=COLORS['secondary'])
        ax.fill_between(fpr_xgb, tpr_xgb, alpha=0.1, color=COLORS['accent'])
        
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1.05])
        ax.set_xlabel('False Positive Rate (1 - Specificity)', fontweight='bold')
        ax.set_ylabel('True Positive Rate (Sensitivity)', fontweight='bold')
        ax.set_title('ROC Curve Comparison\nPatient Readmission Risk Prediction', fontweight='bold', pad=20)
        ax.legend(loc='lower right', fontsize=12, framealpha=0.9)
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/3_roc_curves.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 3_roc_curves.png")

    def plot_4_feature_importance(self):
        """Graph 4: Feature Importance"""
        print("📊 Generating Graph 4: Feature Importance...")
        
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        
        for idx, (name, imp_df, color) in enumerate([
            ('Random Forest', self.results['rf_importance'], COLORS['secondary']),
            ('XGBoost', self.results['xgb_importance'], COLORS['accent'])
        ]):
            bars = axes[idx].barh(imp_df['feature'], imp_df['importance'], color=color, edgecolor='black', linewidth=1)
            axes[idx].set_xlabel('Importance Score', fontweight='bold')
            axes[idx].set_title(f'{name}\nFeature Importance', fontweight='bold', pad=15)
            
            for bar, val in zip(bars, imp_df['importance']):
                axes[idx].text(val + 0.005, bar.get_y() + bar.get_height()/2, f'{val:.3f}',
                              va='center', fontweight='bold', fontsize=11)
        
        plt.suptitle('Feature Importance Analysis - Readmission Prediction', fontweight='bold', fontsize=16, y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/4_feature_importance.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 4_feature_importance.png")

    def plot_5_precision_recall(self):
        """Graph 5: Precision-Recall Comparison"""
        print("📊 Generating Graph 5: Precision-Recall...")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        metrics = ['Precision', 'Recall']
        rf = [self.results['rf']['precision'], self.results['rf']['recall']]
        xgb = [self.results['xgb']['precision'], self.results['xgb']['recall']]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, rf, width, label='Random Forest', color=COLORS['secondary'], edgecolor='black')
        bars2 = ax.bar(x + width/2, xgb, width, label='XGBoost', color=COLORS['accent'], edgecolor='black')
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.1%}', xy=(bar.get_x() + bar.get_width()/2, height),
                           xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold')
        
        ax.set_ylabel('Score', fontweight='bold')
        ax.set_title('Precision vs Recall\nHigh Readmission Risk Detection', fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, fontweight='bold', fontsize=14)
        ax.legend(loc='upper right')
        ax.set_ylim([0, 0.6])
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/5_precision_recall.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 5_precision_recall.png")

    def plot_6_accuracy_f1(self):
        """Graph 6: Accuracy & F1-Score"""
        print("📊 Generating Graph 6: Accuracy & F1...")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        metrics = ['Accuracy', 'F1-Score']
        rf = [self.results['rf']['accuracy'], self.results['rf']['f1']]
        xgb = [self.results['xgb']['accuracy'], self.results['xgb']['f1']]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, rf, width, label='Random Forest', color=COLORS['secondary'], edgecolor='black')
        bars2 = ax.bar(x + width/2, xgb, width, label='XGBoost', color=COLORS['accent'], edgecolor='black')
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.1%}', xy=(bar.get_x() + bar.get_width()/2, height),
                           xytext=(0, 3), textcoords="offset points", ha='center', fontweight='bold')
        
        ax.set_ylabel('Score', fontweight='bold')
        ax.set_title('Overall Performance Metrics', fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, fontweight='bold', fontsize=14)
        ax.legend()
        ax.set_ylim([0, 0.8])
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/6_accuracy_f1.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 6_accuracy_f1.png")

    def plot_7_summary_table(self):
        """Graph 7: Model Summary Table"""
        print("📊 Generating Graph 7: Summary Table...")
        
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.axis('off')
        
        data = [
            ['Accuracy', f"{self.results['rf']['accuracy']:.2%}", f"{self.results['xgb']['accuracy']:.2%}"],
            ['Precision', f"{self.results['rf']['precision']:.2%}", f"{self.results['xgb']['precision']:.2%}"],
            ['Recall', f"{self.results['rf']['recall']:.2%}", f"{self.results['xgb']['recall']:.2%}"],
            ['F1-Score', f"{self.results['rf']['f1']:.2%}", f"{self.results['xgb']['f1']:.2%}"],
            ['ROC-AUC', f"{self.results['rf']['roc_auc']:.4f}", f"{self.results['xgb']['roc_auc']:.4f}"]
        ]
        
        table = ax.table(cellText=data, colLabels=['Metric', 'Random Forest', 'XGBoost'],
                        cellLoc='center', loc='center', colWidths=[0.3, 0.35, 0.35])
        table.auto_set_font_size(False)
        table.set_fontsize(14)
        table.scale(1, 2.5)
        
        for i in range(3):
            table[(0, i)].set_facecolor(COLORS['dark'])
            table[(0, i)].set_text_props(color='white', weight='bold', fontsize=14)
        
        for i in range(1, 6):
            table[(i, 1)].set_facecolor('#d4edda')
            table[(i, 2)].set_facecolor('#cce5ff')
        
        plt.title('Complete Model Comparison Summary', fontweight='bold', fontsize=18, pad=30)
        plt.savefig(f'{self.output_dir}/7_model_summary_table.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 7_model_summary_table.png")

    # ===== NEW GRAPHS (8-14) =====
    
    def plot_8_data_distribution(self):
        """Graph 8: Demographics Distribution"""
        print("📊 Generating Graph 8: Data Distribution...")
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # Age distribution
        age_counts = self.patient_df.groupby('age_group')['patient_count'].sum().sort_index()
        axes[0].bar(range(len(age_counts)), age_counts.values, color=COLORS['primary'], edgecolor='black')
        axes[0].set_xticks(range(len(age_counts)))
        axes[0].set_xticklabels(age_counts.index, rotation=45, ha='right')
        axes[0].set_title('Patients by Age Group', fontweight='bold')
        axes[0].set_ylabel('Patient Count', fontweight='bold')
        
        # Gender distribution
        gender_counts = self.patient_df.groupby('gender')['patient_count'].sum()
        colors_gender = [COLORS['accent'], COLORS['warning']]
        axes[1].pie(gender_counts.values, labels=['Female', 'Male'], autopct='%1.1f%%',
                   colors=colors_gender, explode=(0.02, 0.02), startangle=90)
        axes[1].set_title('Patients by Gender', fontweight='bold')
        
        # Insurance distribution
        ins_counts = self.patient_df.groupby('insurance_type')['patient_count'].sum().sort_values(ascending=True)
        axes[2].barh(ins_counts.index, ins_counts.values, color=COLORS['secondary'], edgecolor='black')
        axes[2].set_title('Patients by Insurance', fontweight='bold')
        axes[2].set_xlabel('Patient Count', fontweight='bold')
        
        plt.suptitle('Patient Demographics Distribution', fontweight='bold', fontsize=16, y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/8_data_distribution.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 8_data_distribution.png")

    def plot_9_readmission_analysis(self):
        """Graph 9: Readmission Rate Analysis"""
        print("📊 Generating Graph 9: Readmission Analysis...")
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        
        # By age group
        age_readm = self.patient_df.groupby('age_group')['readmission_rate'].mean().sort_index()
        bars1 = axes[0].bar(range(len(age_readm)), age_readm.values * 100, color=COLORS['danger'], edgecolor='black')
        axes[0].set_xticks(range(len(age_readm)))
        axes[0].set_xticklabels(age_readm.index, rotation=45, ha='right')
        axes[0].set_title('Readmission Rate by Age Group', fontweight='bold')
        axes[0].set_ylabel('Readmission Rate (%)', fontweight='bold')
        axes[0].axhline(y=20, color='red', linestyle='--', label='High Risk Threshold (20%)')
        axes[0].legend()
        
        for bar in bars1:
            axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                        f'{bar.get_height():.1f}%', ha='center', fontweight='bold', fontsize=10)
        
        # By insurance type
        ins_readm = self.patient_df.groupby('insurance_type')['readmission_rate'].mean().sort_values()
        bars2 = axes[1].barh(ins_readm.index, ins_readm.values * 100, color=COLORS['warning'], edgecolor='black')
        axes[1].axvline(x=20, color='red', linestyle='--', label='High Risk Threshold')
        axes[1].set_title('Readmission Rate by Insurance', fontweight='bold')
        axes[1].set_xlabel('Readmission Rate (%)', fontweight='bold')
        axes[1].legend()
        
        plt.suptitle('Readmission Rate Analysis by Demographics', fontweight='bold', fontsize=16, y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/9_readmission_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 9_readmission_analysis.png")

    def plot_10_physician_trends(self):
        """Graph 10: Physician Performance Trends"""
        print("📊 Generating Graph 10: Physician Trends...")
        
        # Get top 5 physicians by patient volume
        top_physicians = self.physician_df.groupby('physician_id')['total_patients'].sum().nlargest(5).index
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        
        colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warning'], COLORS['danger']]
        
        for i, phy_id in enumerate(top_physicians):
            phy_data = self.physician_df[self.physician_df['physician_id'] == phy_id].sort_values(['year', 'month'])
            phy_data['period'] = phy_data['year'].astype(str) + '-' + phy_data['month'].astype(str).str.zfill(2)
            
            # Sample every 6 months for clarity
            phy_sample = phy_data.iloc[::6]
            name = phy_data['physician_name'].iloc[0].replace('Dr. ', '')
            
            axes[0].plot(range(len(phy_sample)), phy_sample['avg_satisfaction_score'], 
                        marker='o', label=name, color=colors[i], linewidth=2)
            axes[1].plot(range(len(phy_sample)), phy_sample['total_patients'],
                        marker='s', label=name, color=colors[i], linewidth=2)
        
        axes[0].set_title('Satisfaction Score Trends', fontweight='bold')
        axes[0].set_ylabel('Avg Satisfaction (1-5)', fontweight='bold')
        axes[0].legend(loc='lower right')
        axes[0].set_ylim([3, 5])
        
        axes[1].set_title('Patient Volume Trends', fontweight='bold')
        axes[1].set_ylabel('Total Patients', fontweight='bold')
        axes[1].legend(loc='upper right')
        
        plt.suptitle('Top 5 Physicians - Performance Over Time', fontweight='bold', fontsize=16, y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/10_physician_performance_trends.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 10_physician_performance_trends.png")

    def plot_11_department_comparison(self):
        """Graph 11: Department Comparison"""
        print("📊 Generating Graph 11: Department Comparison...")
        
        dept_summary = self.dept_df.groupby('department_name').agg({
            'total_admissions': 'sum',
            'avg_cost': 'mean',
            'occupancy_rate': 'mean'
        }).sort_values('total_admissions', ascending=False).head(10)
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 7))
        
        # Admissions
        axes[0].barh(dept_summary.index, dept_summary['total_admissions'], color=COLORS['primary'], edgecolor='black')
        axes[0].set_title('Total Admissions', fontweight='bold')
        axes[0].set_xlabel('Admissions', fontweight='bold')
        
        # Avg Cost
        axes[1].barh(dept_summary.index, dept_summary['avg_cost'], color=COLORS['warning'], edgecolor='black')
        axes[1].set_title('Average Cost ($)', fontweight='bold')
        axes[1].set_xlabel('Cost ($)', fontweight='bold')
        
        # Occupancy
        axes[2].barh(dept_summary.index, dept_summary['occupancy_rate'] * 100, color=COLORS['secondary'], edgecolor='black')
        axes[2].set_title('Avg Occupancy Rate (%)', fontweight='bold')
        axes[2].set_xlabel('Occupancy %', fontweight='bold')
        axes[2].axvline(x=85, color='red', linestyle='--', alpha=0.7)
        
        plt.suptitle('Department Performance Comparison (Top 10)', fontweight='bold', fontsize=16, y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/11_department_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 11_department_comparison.png")

    def plot_12_financial_trends(self):
        """Graph 12: Financial Trends"""
        print("📊 Generating Graph 12: Financial Trends...")
        
        self.financial_df['period'] = self.financial_df['year'].astype(str) + '-' + self.financial_df['month'].astype(str).str.zfill(2)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Revenue & Expenses
        axes[0,0].plot(range(len(self.financial_df)), self.financial_df['total_revenue']/1e6, 
                      marker='o', color=COLORS['secondary'], label='Revenue', linewidth=2)
        axes[0,0].plot(range(len(self.financial_df)), self.financial_df['total_expenses']/1e6,
                      marker='s', color=COLORS['danger'], label='Expenses', linewidth=2)
        axes[0,0].set_title('Revenue vs Expenses (Monthly)', fontweight='bold')
        axes[0,0].set_ylabel('Amount ($ Millions)', fontweight='bold')
        axes[0,0].legend()
        axes[0,0].fill_between(range(len(self.financial_df)), 
                               self.financial_df['total_revenue']/1e6,
                               self.financial_df['total_expenses']/1e6, alpha=0.2, color='green')
        
        # Net Income
        axes[0,1].bar(range(len(self.financial_df)), self.financial_df['net_income']/1e6,
                     color=[COLORS['secondary'] if x > 0 else COLORS['danger'] for x in self.financial_df['net_income']])
        axes[0,1].set_title('Net Income (Monthly)', fontweight='bold')
        axes[0,1].set_ylabel('Net Income ($ Millions)', fontweight='bold')
        axes[0,1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        # Operating Margin
        axes[1,0].plot(range(len(self.financial_df)), self.financial_df['operating_margin']*100,
                      marker='o', color=COLORS['accent'], linewidth=2)
        axes[1,0].axhline(y=15, color='orange', linestyle='--', label='Target (15%)')
        axes[1,0].set_title('Operating Margin Trend', fontweight='bold')
        axes[1,0].set_ylabel('Operating Margin (%)', fontweight='bold')
        axes[1,0].legend()
        
        # Cash on Hand
        axes[1,1].fill_between(range(len(self.financial_df)), self.financial_df['cash_on_hand']/1e6,
                              color=COLORS['primary'], alpha=0.6)
        axes[1,1].plot(range(len(self.financial_df)), self.financial_df['cash_on_hand']/1e6,
                      color=COLORS['primary'], linewidth=2)
        axes[1,1].set_title('Cash on Hand', fontweight='bold')
        axes[1,1].set_ylabel('Cash ($ Millions)', fontweight='bold')
        
        plt.suptitle('Financial Performance Dashboard (2022-2024)', fontweight='bold', fontsize=16, y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/12_financial_trends.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 12_financial_trends.png")

    def plot_13_correlation_heatmap(self):
        """Graph 13: Correlation Heatmap"""
        print("📊 Generating Graph 13: Correlation Heatmap...")
        
        numeric_cols = ['patient_count', 'avg_length_of_stay', 'avg_cost', 'readmission_rate']
        corr_matrix = self.patient_df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.3f', cmap='RdBu_r',
                   center=0, square=True, linewidths=2,
                   cbar_kws={'shrink': 0.8, 'label': 'Correlation'},
                   annot_kws={'size': 14, 'weight': 'bold'})
        
        plt.title('Feature Correlation Matrix\nPatient Demographics Dataset', fontweight='bold', fontsize=14, pad=20)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/13_correlation_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 13_correlation_heatmap.png")

    def plot_14_cost_analysis(self):
        """Graph 14: Cost Analysis"""
        print("📊 Generating Graph 14: Cost Analysis...")
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        
        # Cost by insurance
        ins_cost = self.patient_df.groupby('insurance_type')['avg_cost'].mean().sort_values()
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(ins_cost)))
        axes[0].barh(ins_cost.index, ins_cost.values, color=colors, edgecolor='black')
        axes[0].set_title('Average Cost by Insurance Type', fontweight='bold')
        axes[0].set_xlabel('Average Cost ($)', fontweight='bold')
        
        for i, (idx, val) in enumerate(ins_cost.items()):
            axes[0].text(val + 100, i, f'${val:,.0f}', va='center', fontweight='bold', fontsize=9)
        
        # Cost by age group
        age_cost = self.patient_df.groupby('age_group')['avg_cost'].mean().sort_index()
        bars = axes[1].bar(range(len(age_cost)), age_cost.values, color=COLORS['accent'], edgecolor='black')
        axes[1].set_xticks(range(len(age_cost)))
        axes[1].set_xticklabels(age_cost.index, rotation=45, ha='right')
        axes[1].set_title('Average Cost by Age Group', fontweight='bold')
        axes[1].set_ylabel('Average Cost ($)', fontweight='bold')
        
        for bar in bars:
            axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                        f'${bar.get_height():,.0f}', ha='center', fontweight='bold', fontsize=10)
        
        plt.suptitle('Healthcare Cost Analysis', fontweight='bold', fontsize=16, y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/14_cost_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"   ✅ Saved: 14_cost_analysis.png")

    def generate_all(self):
        """Generate all 14 visualizations"""
        print("\n" + "="*70)
        print("🎨 GENERATING ALL 14 VISUALIZATIONS")
        print("="*70)
        
        # ML-dependent graphs (1-7)
        if self.results:
            self.plot_1_model_comparison()
            self.plot_2_confusion_matrices()
            self.plot_3_roc_curves()
            self.plot_4_feature_importance()
            self.plot_5_precision_recall()
            self.plot_6_accuracy_f1()
            self.plot_7_summary_table()
        
        # Data-dependent graphs (8-14)
        self.plot_8_data_distribution()
        self.plot_9_readmission_analysis()
        self.plot_10_physician_trends()
        self.plot_11_department_comparison()
        self.plot_12_financial_trends()
        self.plot_13_correlation_heatmap()
        self.plot_14_cost_analysis()
        
        print("\n" + "="*70)
        print("✅ ALL VISUALIZATIONS GENERATED!")
        print("="*70)
        print(f"\n📁 Output: {self.output_dir}/")


if __name__ == "__main__":
    print("\n🚀 HEALTHCARE VISUALIZATION PIPELINE")
    print("="*70)
    
    # Get absolute path for data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'patient_demographics.csv')
    
    # Run ML pipeline
    print("\n📊 Step 1: Running ML Pipeline...")
    pipeline = HealthcarePredictiveModel(data_path)
    results = pipeline.run_complete_pipeline()
    
    # Generate all visualizations
    print("\n🎨 Step 2: Generating Visualizations...")
    viz = ComprehensiveVisualizer(pipeline, results)
    viz.generate_all()
    
    print("\n✅ COMPLETE!")
