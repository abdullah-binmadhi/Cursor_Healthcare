"""
Healthcare ML Visualization - Generate All Graphs
Creates comprehensive visualizations for Random Forest vs XGBoost comparison
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our pipeline
from healthcare_ml_pipeline import HealthcarePredictiveModel

# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

class MLVisualizer:
    """
    Generate all ML model visualizations
    """
    
    def __init__(self, pipeline, results):
        self.pipeline = pipeline
        self.results = results
        self.output_dir = 'graphs'
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def plot_model_comparison_metrics(self):
        """Plot 1: Model Comparison - All Metrics"""
        print("\n📊 Generating Graph 1: Model Comparison Metrics...")
        
        metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        rf_scores = [self.results['rf'][m] for m in metrics]
        xgb_scores = [self.results['xgb'][m] for m in metrics]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars1 = ax.bar(x - width/2, rf_scores, width, label='Random Forest', 
                       color='#2ecc71', alpha=0.8, edgecolor='black')
        bars2 = ax.bar(x + width/2, xgb_scores, width, label='XGBoost', 
                       color='#3498db', alpha=0.8, edgecolor='black')
        
        ax.set_xlabel('Metrics', fontsize=14, fontweight='bold')
        ax.set_ylabel('Score', fontsize=14, fontweight='bold')
        ax.set_title('Healthcare Readmission Prediction\nRandom Forest vs XGBoost - Performance Comparison', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC'], 
                          fontsize=12, fontweight='bold')
        ax.legend(fontsize=12, loc='lower right')
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/1_model_comparison_metrics.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: {self.output_dir}/1_model_comparison_metrics.png")
    
    def plot_confusion_matrices(self):
        """Plot 2: Confusion Matrices for Both Models"""
        print("\n📊 Generating Graph 2: Confusion Matrices...")
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        models = [
            ('Random Forest', self.results['rf']['y_pred'], '#2ecc71'),
            ('XGBoost', self.results['xgb']['y_pred'], '#3498db')
        ]
        
        for idx, (name, y_pred, color) in enumerate(models):
            cm = confusion_matrix(self.pipeline.y_test, y_pred)
            
            # Normalize confusion matrix
            cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            
            # Plot
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       cbar_kws={'label': 'Count'}, square=True,
                       xticklabels=['Low Risk', 'High Risk'],
                       yticklabels=['Low Risk', 'High Risk'])
            
            axes[idx].set_title(f'{name}\nConfusion Matrix', fontsize=14, fontweight='bold', pad=15)
            axes[idx].set_ylabel('True Label', fontsize=12, fontweight='bold')
            axes[idx].set_xlabel('Predicted Label', fontsize=12, fontweight='bold')
            
            # Add percentages
            for i in range(2):
                for j in range(2):
                    text = axes[idx].text(j + 0.5, i + 0.7, 
                                         f'({cm_normalized[i, j]*100:.1f}%)',
                                         ha="center", va="center", fontsize=10, color='red')
        
        plt.suptitle('Confusion Matrix Comparison - Patient Readmission Risk', 
                     fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/2_confusion_matrices.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: {self.output_dir}/2_confusion_matrices.png")
    
    def plot_roc_curves(self):
        """Plot 3: ROC Curves Comparison"""
        print("\n📊 Generating Graph 3: ROC Curves...")
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Random Forest ROC
        fpr_rf, tpr_rf, _ = roc_curve(self.pipeline.y_test, self.results['rf']['y_pred_proba'])
        roc_auc_rf = auc(fpr_rf, tpr_rf)
        
        # XGBoost ROC
        fpr_xgb, tpr_xgb, _ = roc_curve(self.pipeline.y_test, self.results['xgb']['y_pred_proba'])
        roc_auc_xgb = auc(fpr_xgb, tpr_xgb)
        
        # Plot
        ax.plot(fpr_rf, tpr_rf, color='#2ecc71', lw=3, 
                label=f'Random Forest (AUC = {roc_auc_rf:.3f})')
        ax.plot(fpr_xgb, tpr_xgb, color='#3498db', lw=3, 
                label=f'XGBoost (AUC = {roc_auc_xgb:.3f})')
        ax.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--', 
                label='Random Classifier (AUC = 0.500)')
        
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate', fontsize=14, fontweight='bold')
        ax.set_ylabel('True Positive Rate', fontsize=14, fontweight='bold')
        ax.set_title('ROC Curve Comparison\nPatient Readmission Risk Prediction', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc="lower right", fontsize=12, framealpha=0.9)
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/3_roc_curves.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: {self.output_dir}/3_roc_curves.png")
    
    def plot_feature_importance_comparison(self):
        """Plot 4: Feature Importance Comparison"""
        print("\n📊 Generating Graph 4: Feature Importance Comparison...")
        
        rf_imp = self.results['rf_importance']
        xgb_imp = self.results['xgb_importance']
        
        fig, axes = plt.subplots(1, 2, figsize=(18, 7))
        
        # Random Forest
        axes[0].barh(rf_imp['feature'], rf_imp['importance'], color='#2ecc71', 
                    alpha=0.8, edgecolor='black')
        axes[0].set_xlabel('Importance', fontsize=12, fontweight='bold')
        axes[0].set_title('Random Forest\nFeature Importance', fontsize=14, fontweight='bold', pad=15)
        axes[0].grid(axis='x', alpha=0.3)
        
        # Add value labels
        for idx, (feat, imp) in enumerate(zip(rf_imp['feature'], rf_imp['importance'])):
            axes[0].text(imp, idx, f' {imp:.3f}', va='center', fontsize=10, fontweight='bold')
        
        # XGBoost
        axes[1].barh(xgb_imp['feature'], xgb_imp['importance'], color='#3498db', 
                    alpha=0.8, edgecolor='black')
        axes[1].set_xlabel('Importance', fontsize=12, fontweight='bold')
        axes[1].set_title('XGBoost\nFeature Importance', fontsize=14, fontweight='bold', pad=15)
        axes[1].grid(axis='x', alpha=0.3)
        
        # Add value labels
        for idx, (feat, imp) in enumerate(zip(xgb_imp['feature'], xgb_imp['importance'])):
            axes[1].text(imp, idx, f' {imp:.3f}', va='center', fontsize=10, fontweight='bold')
        
        plt.suptitle('Feature Importance Analysis - Patient Readmission Prediction', 
                     fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/4_feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: {self.output_dir}/4_feature_importance.png")
    
    def plot_precision_recall_comparison(self):
        """Plot 5: Precision-Recall Bar Chart"""
        print("\n📊 Generating Graph 5: Precision-Recall Comparison...")
        
        metrics = ['Precision', 'Recall']
        rf_scores = [self.results['rf']['precision'], self.results['rf']['recall']]
        xgb_scores = [self.results['xgb']['precision'], self.results['xgb']['recall']]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars1 = ax.bar(x - width/2, rf_scores, width, label='Random Forest', 
                       color='#2ecc71', alpha=0.8, edgecolor='black')
        bars2 = ax.bar(x + width/2, xgb_scores, width, label='XGBoost', 
                       color='#3498db', alpha=0.8, edgecolor='black')
        
        ax.set_ylabel('Score', fontsize=14, fontweight='bold')
        ax.set_title('Precision vs Recall Comparison\nHigh Readmission Risk Detection', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, fontsize=13, fontweight='bold')
        ax.legend(fontsize=12, loc='lower right')
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}\n({height*100:.1f}%)',
                       ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Add interpretation text
        ax.text(0.5, 0.02, 
                'Precision: Of predicted high-risk patients, how many were actually high-risk?\n' +
                'Recall: Of actual high-risk patients, how many did we identify?',
                transform=ax.transAxes, fontsize=10, style='italic',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3),
                horizontalalignment='center')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/5_precision_recall.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: {self.output_dir}/5_precision_recall.png")
    
    def plot_accuracy_f1_comparison(self):
        """Plot 6: Accuracy and F1-Score Comparison"""
        print("\n📊 Generating Graph 6: Accuracy & F1-Score Comparison...")
        
        metrics = ['Accuracy', 'F1-Score']
        rf_scores = [self.results['rf']['accuracy'], self.results['rf']['f1']]
        xgb_scores = [self.results['xgb']['accuracy'], self.results['xgb']['f1']]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars1 = ax.bar(x - width/2, rf_scores, width, label='Random Forest', 
                       color='#2ecc71', alpha=0.8, edgecolor='black')
        bars2 = ax.bar(x + width/2, xgb_scores, width, label='XGBoost', 
                       color='#3498db', alpha=0.8, edgecolor='black')
        
        ax.set_ylabel('Score', fontsize=14, fontweight='bold')
        ax.set_title('Overall Performance Metrics\nAccuracy & F1-Score Comparison', 
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, fontsize=13, fontweight='bold')
        ax.legend(fontsize=12, loc='lower right')
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}\n({height*100:.1f}%)',
                       ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Add interpretation
        ax.text(0.5, 0.02, 
                'Accuracy: Overall correct predictions | F1-Score: Harmonic mean of Precision & Recall',
                transform=ax.transAxes, fontsize=10, style='italic',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3),
                horizontalalignment='center')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/6_accuracy_f1.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: {self.output_dir}/6_accuracy_f1.png")
    
    def plot_model_summary_table(self):
        """Plot 7: Model Comparison Summary Table"""
        print("\n📊 Generating Graph 7: Model Summary Table...")
        
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.axis('tight')
        ax.axis('off')
        
        # Prepare data
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
        rf_vals = [
            f"{self.results['rf']['accuracy']:.4f} ({self.results['rf']['accuracy']*100:.2f}%)",
            f"{self.results['rf']['precision']:.4f} ({self.results['rf']['precision']*100:.2f}%)",
            f"{self.results['rf']['recall']:.4f} ({self.results['rf']['recall']*100:.2f}%)",
            f"{self.results['rf']['f1']:.4f}",
            f"{self.results['rf']['roc_auc']:.4f}"
        ]
        xgb_vals = [
            f"{self.results['xgb']['accuracy']:.4f} ({self.results['xgb']['accuracy']*100:.2f}%)",
            f"{self.results['xgb']['precision']:.4f} ({self.results['xgb']['precision']*100:.2f}%)",
            f"{self.results['xgb']['recall']:.4f} ({self.results['xgb']['recall']*100:.2f}%)",
            f"{self.results['xgb']['f1']:.4f}",
            f"{self.results['xgb']['roc_auc']:.4f}"
        ]
        
        # Create table
        table_data = []
        for i, metric in enumerate(metrics):
            rf_val = float(rf_vals[i].split()[0])
            xgb_val = float(xgb_vals[i].split()[0])
            winner = "🏆 RF" if rf_val > xgb_val else "🏆 XGB" if xgb_val > rf_val else "🤝 Tie"
            table_data.append([metric, rf_vals[i], xgb_vals[i], winner])
        
        table = ax.table(cellText=table_data,
                        colLabels=['Metric', 'Random Forest', 'XGBoost', 'Winner'],
                        cellLoc='center',
                        loc='center',
                        colWidths=[0.2, 0.3, 0.3, 0.2])
        
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 3)
        
        # Style header
        for i in range(4):
            table[(0, i)].set_facecolor('#34495e')
            table[(0, i)].set_text_props(weight='bold', color='white', fontsize=13)
        
        # Style cells
        for i in range(1, len(metrics) + 1):
            for j in range(4):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#ecf0f1')
                table[(i, j)].set_text_props(fontsize=11)
                
                # Highlight winner column
                if j == 3:
                    table[(i, j)].set_facecolor('#f39c12')
                    table[(i, j)].set_text_props(weight='bold')
        
        plt.title('Healthcare Readmission Prediction - Complete Model Comparison\n' +
                 'Random Forest vs XGBoost Performance Metrics',
                 fontsize=16, fontweight='bold', pad=20)
        
        plt.savefig(f'{self.output_dir}/7_model_summary_table.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: {self.output_dir}/7_model_summary_table.png")
    
    def generate_all_visualizations(self):
        """Generate all visualizations"""
        print("\n" + "=" * 70)
        print("📊 GENERATING ALL VISUALIZATIONS")
        print("=" * 70)
        
        self.plot_model_comparison_metrics()
        self.plot_confusion_matrices()
        self.plot_roc_curves()
        self.plot_feature_importance_comparison()
        self.plot_precision_recall_comparison()
        self.plot_accuracy_f1_comparison()
        self.plot_model_summary_table()
        
        print("\n" + "=" * 70)
        print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
        print("=" * 70)
        print(f"\n📁 Output Directory: {self.output_dir}/")
        print(f"   7 PNG graphs created")
        print(f"   Resolution: 300 DPI (publication quality)")

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🎨 HEALTHCARE ML VISUALIZATION PIPELINE")
    print("=" * 70)
    
    # Run ML pipeline
    print("\nStep 1: Running ML Pipeline...")
    pipeline = HealthcarePredictiveModel('data/patient_demographics.csv')
    results = pipeline.run_complete_pipeline()
    
    # Generate visualizations
    print("\nStep 2: Generating Visualizations...")
    visualizer = MLVisualizer(pipeline, results)
    visualizer.generate_all_visualizations()
    
    print("\n✅ COMPLETE PIPELINE EXECUTED SUCCESSFULLY!")
    print(f"\n📊 Check the 'graphs/' folder for all PNG visualizations")
