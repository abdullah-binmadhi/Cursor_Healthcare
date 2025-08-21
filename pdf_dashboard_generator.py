#!/usr/bin/env python3
"""
Healthcare Analytics PDF Dashboard Generator
Creates downloadable PDF reports from CSV data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime
import numpy as np

class HealthcarePDFDashboard:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        
    def setup_styles(self):
        """Setup custom styles for the PDF"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
    def load_data(self):
        """Load all available CSV files"""
        data_files = {}
        
        csv_files = [
            'healthcare_dataset.csv',
            'healthcare_dataset_enriched.csv',
            'physician_performance.csv',
            'department_metrics.csv',
            'quality_metrics.csv',
            'financial_performance.csv',
            'patient_demographics.csv'
        ]
        
        for file in csv_files:
            if os.path.exists(file):
                try:
                    data_files[file] = pd.read_csv(file)
                    print(f"✓ Loaded {file}")
                except Exception as e:
                    print(f"✗ Error loading {file}: {e}")
            else:
                print(f"✗ File not found: {file}")
                
        return data_files
    
    def create_charts(self, data_files):
        """Create charts and save them as images"""
        charts = {}
        
        # Set style for better looking charts
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Main dataset charts
        if 'healthcare_dataset.csv' in data_files:
            df = data_files['healthcare_dataset.csv']
            
            # Gender distribution pie chart
            plt.figure(figsize=(8, 6))
            gender_counts = df['Gender'].value_counts()
            plt.pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
            plt.title('Patient Gender Distribution', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig('gender_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            charts['gender_dist'] = 'gender_distribution.png'
            
            # Age distribution histogram
            plt.figure(figsize=(10, 6))
            plt.hist(df['Age'], bins=20, edgecolor='black', alpha=0.7)
            plt.title('Patient Age Distribution', fontsize=14, fontweight='bold')
            plt.xlabel('Age')
            plt.ylabel('Number of Patients')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('age_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            charts['age_dist'] = 'age_distribution.png'
            
            # Billing amount distribution
            plt.figure(figsize=(10, 6))
            plt.hist(df['Billing Amount'], bins=30, edgecolor='black', alpha=0.7)
            plt.title('Billing Amount Distribution', fontsize=14, fontweight='bold')
            plt.xlabel('Billing Amount ($)')
            plt.ylabel('Number of Patients')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('billing_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            charts['billing_dist'] = 'billing_distribution.png'
            
            # Medical conditions bar chart
            plt.figure(figsize=(12, 8))
            condition_counts = df['Medical Condition'].value_counts().head(10)
            condition_counts.plot(kind='bar')
            plt.title('Top 10 Medical Conditions', fontsize=14, fontweight='bold')
            plt.xlabel('Medical Condition')
            plt.ylabel('Number of Patients')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('medical_conditions.png', dpi=300, bbox_inches='tight')
            plt.close()
            charts['conditions'] = 'medical_conditions.png'
        
        # Physician performance chart
        if 'physician_performance.csv' in data_files:
            df_phys = data_files['physician_performance.csv']
            plt.figure(figsize=(12, 8))
            # Group by physician and get average satisfaction score
            physician_avg = df_phys.groupby('physician_name')['avg_satisfaction_score'].mean().sort_values(ascending=False).head(10)
            plt.barh(physician_avg.index, physician_avg.values)
            plt.title('Top 10 Physicians by Average Patient Satisfaction', fontsize=14, fontweight='bold')
            plt.xlabel('Average Patient Satisfaction Score')
            plt.tight_layout()
            plt.savefig('physician_satisfaction.png', dpi=300, bbox_inches='tight')
            plt.close()
            charts['physician_sat'] = 'physician_satisfaction.png'
        
        # Department metrics chart
        if 'department_metrics.csv' in data_files:
            df_dept = data_files['department_metrics.csv']
            plt.figure(figsize=(12, 8))
            # Group by department and get average length of stay
            dept_avg = df_dept.groupby('department_name')['avg_length_of_stay'].mean().sort_values(ascending=False)
            plt.bar(dept_avg.index, dept_avg.values)
            plt.title('Average Length of Stay by Department', fontsize=14, fontweight='bold')
            plt.xlabel('Department')
            plt.ylabel('Average Length of Stay (days)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('department_los.png', dpi=300, bbox_inches='tight')
            plt.close()
            charts['dept_los'] = 'department_los.png'
        
        return charts
    
    def create_summary_table(self, data_files):
        """Create summary statistics table"""
        if 'healthcare_dataset.csv' not in data_files:
            return []
        
        df = data_files['healthcare_dataset.csv']
        
        # Calculate summary statistics
        total_patients = len(df)
        avg_age = round(df['Age'].mean(), 1)
        total_revenue = df['Billing Amount'].sum()
        avg_billing = round(df['Billing Amount'].mean(), 2)
        male_count = len(df[df['Gender'] == 'Male'])
        female_count = len(df[df['Gender'] == 'Female'])
        
        # Create table data
        table_data = [
            ['Metric', 'Value'],
            ['Total Patients', f"{total_patients:,}"],
            ['Average Age', f"{avg_age} years"],
            ['Total Revenue', f"${total_revenue:,.2f}"],
            ['Average Billing', f"${avg_billing:,.2f}"],
            ['Male Patients', f"{male_count:,}"],
            ['Female Patients', f"{female_count:,}"],
            ['Report Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        return table_data
    
    def create_recent_data_table(self, data_files):
        """Create table with recent patient data"""
        if 'healthcare_dataset.csv' not in data_files:
            return []
        
        df = data_files['healthcare_dataset.csv']
        
        # Get recent 10 records
        recent_data = df.head(10)[['Name', 'Age', 'Gender', 'Medical Condition', 'Billing Amount']]
        
        # Prepare table data
        table_data = [['Name', 'Age', 'Gender', 'Medical Condition', 'Billing Amount']]
        
        for _, row in recent_data.iterrows():
            table_data.append([
                str(row['Name']),
                str(row['Age']),
                str(row['Gender']),
                str(row['Medical Condition']),
                f"${row['Billing Amount']:,.2f}"
            ])
        
        return table_data
    
    def generate_pdf(self, filename='healthcare_analytics_report.pdf'):
        """Generate the complete PDF report"""
        print("📊 Generating Healthcare Analytics PDF Report...")
        
        # Load data
        data_files = self.load_data()
        if not data_files:
            print("❌ No data files found!")
            return
        
        # Create charts
        print("📈 Creating charts...")
        charts = self.create_charts(data_files)
        
        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title
        story.append(Paragraph("🏥 Healthcare Analytics Dashboard Report", self.title_style))
        story.append(Spacer(1, 20))
        
        # Summary Statistics
        story.append(Paragraph("📊 Summary Statistics", self.heading_style))
        summary_table = self.create_summary_table(data_files)
        if summary_table:
            table = Table(summary_table, colWidths=[2*inch, 3*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
            ]))
            story.append(table)
            story.append(Spacer(1, 20))
        
        # Charts
        if charts:
            story.append(Paragraph("📈 Analytics Charts", self.heading_style))
            
            # Gender Distribution
            if 'gender_dist' in charts:
                story.append(Paragraph("Patient Gender Distribution", self.heading_style))
                story.append(Image(charts['gender_dist'], width=4*inch, height=3*inch))
                story.append(Spacer(1, 10))
            
            # Age Distribution
            if 'age_dist' in charts:
                story.append(Paragraph("Patient Age Distribution", self.heading_style))
                story.append(Image(charts['age_dist'], width=5*inch, height=3*inch))
                story.append(Spacer(1, 10))
            
            # Medical Conditions
            if 'conditions' in charts:
                story.append(Paragraph("Top Medical Conditions", self.heading_style))
                story.append(Image(charts['conditions'], width=5*inch, height=4*inch))
                story.append(Spacer(1, 10))
            
            # Physician Performance
            if 'physician_sat' in charts:
                story.append(Paragraph("Physician Performance", self.heading_style))
                story.append(Image(charts['physician_sat'], width=5*inch, height=4*inch))
                story.append(Spacer(1, 10))
            
            # Department Metrics
            if 'dept_los' in charts:
                story.append(Paragraph("Department Performance", self.heading_style))
                story.append(Image(charts['dept_los'], width=5*inch, height=4*inch))
                story.append(Spacer(1, 10))
        
        # Recent Data Table
        story.append(Paragraph("📋 Recent Patient Data", self.heading_style))
        recent_table = self.create_recent_data_table(data_files)
        if recent_table:
            table = Table(recent_table, colWidths=[1.2*inch, 0.5*inch, 0.6*inch, 2*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            story.append(table)
        
        # Build PDF
        print("📄 Building PDF...")
        doc.build(story)
        
        # Clean up chart files
        for chart_file in charts.values():
            if os.path.exists(chart_file):
                os.remove(chart_file)
        
        print(f"✅ PDF Report generated successfully: {filename}")
        print(f"📁 File location: {os.path.abspath(filename)}")

def main():
    """Main function to generate the PDF dashboard"""
    generator = HealthcarePDFDashboard()
    generator.generate_pdf()

if __name__ == "__main__":
    main()
