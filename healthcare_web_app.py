#!/usr/bin/env python3
"""
Healthcare Analytics Web Application
A comprehensive web dashboard for healthcare analytics and data management
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import pandas as pd
import sqlite3
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
from collections import defaultdict

# Import our pipeline components
try:
    from healthcare_pipeline import HealthcarePipeline, PipelineConfig, DataValidator, DataTransformer
    from pipeline_scheduler import PipelineScheduler, PipelineMonitor
    PIPELINE_AVAILABLE = True
except ImportError:
    print("Pipeline components not available, running in demo mode")
    PIPELINE_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'healthcare_analytics_secret_key_2024'

# Global variables
DATABASE_PATH = 'healthcare_analytics.db'
CSV_PATH = 'healthcare_dataset.csv'

class HealthcareDataManager:
    """Manages healthcare data operations"""
    
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        
    def get_database_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_patient_count(self):
        """Get total patient count"""
        conn = self.get_database_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM patients")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_admission_count(self):
        """Get total admission count"""
        conn = self.get_database_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM admissions")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_financial_summary(self):
        """Get financial summary"""
        conn = self.get_database_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                SUM(total_charges) as total_charges,
                SUM(insurance_payment) as insurance_payments,
                SUM(patient_payment) as patient_payments,
                SUM(net_revenue) as net_revenue,
                AVG(total_charges) as avg_charge
            FROM financial_data
        """)
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total_charges': result[0] or 0,
            'insurance_payments': result[1] or 0,
            'patient_payments': result[2] or 0,
            'net_revenue': result[3] or 0,
            'avg_charge': result[4] or 0
        }
    
    def get_recent_admissions(self, limit=10):
        """Get recent admissions"""
        conn = self.get_database_connection()
        df = pd.read_sql_query("""
            SELECT 
                a.admission_id,
                p.first_name || ' ' || p.last_name as patient_name,
                a.admission_date,
                a.discharge_date,
                a.admission_type,
                a.attending_physician,
                fd.total_charges,
                fd.net_revenue
            FROM admissions a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN financial_data fd ON a.admission_id = fd.admission_id
            ORDER BY a.admission_date DESC
            LIMIT ?
        """, conn, params=[limit])
        conn.close()
        return df
    
    def get_top_diagnoses(self, limit=5):
        """Get top diagnoses"""
        conn = self.get_database_connection()
        df = pd.read_sql_query("""
            SELECT 
                d.diagnosis_description,
                COUNT(*) as case_count,
                AVG(a.length_of_stay) as avg_los,
                AVG(fd.net_revenue) as avg_revenue
            FROM diagnoses d
            JOIN admissions a ON d.admission_id = a.admission_id
            JOIN financial_data fd ON a.admission_id = fd.admission_id
            WHERE d.diagnosis_type = 'Primary'
            GROUP BY d.diagnosis_description
            ORDER BY case_count DESC
            LIMIT ?
        """, conn, params=[limit])
        conn.close()
        return df
    
    def get_physician_performance(self, limit=10):
        """Get physician performance"""
        conn = self.get_database_connection()
        df = pd.read_sql_query("""
            SELECT 
                physician_name,
                SUM(total_patients) as total_patients,
                AVG(avg_length_of_stay) as avg_los,
                AVG(avg_satisfaction_score) as avg_satisfaction,
                AVG(complication_rate) as complication_rate,
                AVG(readmission_rate) as readmission_rate,
                AVG(avg_revenue) as avg_revenue
            FROM physician_performance
            GROUP BY physician_name
            ORDER BY total_patients DESC
            LIMIT ?
        """, conn, params=[limit])
        conn.close()
        return df
    
    def get_department_metrics(self):
        """Get department metrics"""
        conn = self.get_database_connection()
        df = pd.read_sql_query("""
            SELECT 
                department_name,
                SUM(total_admissions) as total_admissions,
                AVG(avg_length_of_stay) as avg_los,
                AVG(avg_cost) as avg_cost,
                SUM(total_revenue) as total_revenue,
                AVG(occupancy_rate) as occupancy_rate
            FROM department_metrics
            GROUP BY department_name
            ORDER BY total_admissions DESC
        """, conn)
        conn.close()
        return df
    
    def get_quality_metrics(self):
        """Get quality metrics"""
        conn = self.get_database_connection()
        df = pd.read_sql_query("""
            SELECT 
                month,
                year,
                hospital_acquired_infections,
                pressure_ulcers,
                falls,
                medication_errors,
                patient_satisfaction_avg,
                readmission_rate,
                mortality_rate,
                avg_length_of_stay
            FROM quality_metrics
            ORDER BY year DESC, month DESC
            LIMIT 12
        """, conn)
        conn.close()
        return df
    
    def get_financial_performance(self):
        """Get financial performance"""
        conn = self.get_database_connection()
        df = pd.read_sql_query("""
            SELECT 
                month,
                year,
                total_revenue,
                total_expenses,
                net_income,
                operating_margin,
                bad_debt,
                charity_care
            FROM financial_performance
            ORDER BY year DESC, month DESC
            LIMIT 12
        """, conn)
        conn.close()
        return df

# Initialize data manager
data_manager = HealthcareDataManager()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    try:
        # Get key metrics
        patient_count = data_manager.get_patient_count()
        admission_count = data_manager.get_admission_count()
        financial_summary = data_manager.get_financial_summary()
        
        # Get recent admissions
        recent_admissions = data_manager.get_recent_admissions(10)
        
        # Get top diagnoses
        top_diagnoses = data_manager.get_top_diagnoses(5)
        
        # Get physician performance
        physician_performance = data_manager.get_physician_performance(5)
        
        return render_template('dashboard.html',
                             patient_count=patient_count,
                             admission_count=admission_count,
                             financial_summary=financial_summary,
                             recent_admissions=recent_admissions.to_dict('records'),
                             top_diagnoses=top_diagnoses.to_dict('records'),
                             physician_performance=physician_performance.to_dict('records'))
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", 'error')
        return render_template('dashboard.html', error=True)

@app.route('/analytics')
def analytics():
    """Analytics page"""
    try:
        # Get analytics data
        department_metrics = data_manager.get_department_metrics()
        quality_metrics = data_manager.get_quality_metrics()
        financial_performance = data_manager.get_financial_performance()
        
        return render_template('analytics.html',
                             department_metrics=department_metrics.to_dict('records'),
                             quality_metrics=quality_metrics.to_dict('records'),
                             financial_performance=financial_performance.to_dict('records'))
    except Exception as e:
        flash(f"Error loading analytics: {str(e)}", 'error')
        return render_template('analytics.html', error=True)

@app.route('/patients')
def patients():
    """Patients page"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 50
        offset = (page - 1) * per_page
        
        conn = data_manager.get_database_connection()
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM patients")
        total_count = cursor.fetchone()[0]
        
        # Get patients with pagination
        cursor.execute("""
            SELECT 
                patient_id,
                first_name,
                last_name,
                date_of_birth,
                gender,
                insurance_type,
                created_date
            FROM patients
            ORDER BY created_date DESC
            LIMIT ? OFFSET ?
        """, [per_page, offset])
        
        patients = cursor.fetchall()
        conn.close()
        
        # Calculate pagination
        total_pages = (total_count + per_page - 1) // per_page
        
        return render_template('patients.html',
                             patients=patients,
                             current_page=page,
                             total_pages=total_pages,
                             total_count=total_count)
    except Exception as e:
        flash(f"Error loading patients: {str(e)}", 'error')
        return render_template('patients.html', error=True)

@app.route('/admissions')
def admissions():
    """Admissions page"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 50
        offset = (page - 1) * per_page
        
        conn = data_manager.get_database_connection()
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM admissions")
        total_count = cursor.fetchone()[0]
        
        # Get admissions with pagination
        cursor.execute("""
            SELECT 
                a.admission_id,
                p.first_name || ' ' || p.last_name as patient_name,
                a.admission_date,
                a.discharge_date,
                a.admission_type,
                a.department,
                a.attending_physician,
                a.length_of_stay,
                fd.total_charges,
                fd.net_revenue
            FROM admissions a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN financial_data fd ON a.admission_id = fd.admission_id
            ORDER BY a.admission_date DESC
            LIMIT ? OFFSET ?
        """, [per_page, offset])
        
        admissions = cursor.fetchall()
        conn.close()
        
        # Calculate pagination
        total_pages = (total_count + per_page - 1) // per_page
        
        return render_template('admissions.html',
                             admissions=admissions,
                             current_page=page,
                             total_pages=total_pages,
                             total_count=total_count)
    except Exception as e:
        flash(f"Error loading admissions: {str(e)}", 'error')
        return render_template('admissions.html', error=True)

@app.route('/pipeline')
def pipeline():
    """Pipeline management page"""
    try:
        return render_template('pipeline.html', pipeline_available=PIPELINE_AVAILABLE)
    except Exception as e:
        flash(f"Error loading pipeline page: {str(e)}", 'error')
        return render_template('pipeline.html', error=True)

@app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    """Run the healthcare pipeline"""
    try:
        if not PIPELINE_AVAILABLE:
            flash("Pipeline components not available", 'error')
            return redirect(url_for('pipeline'))
        
        # Run pipeline
        config = PipelineConfig(
            source_type='csv',
            source_path=CSV_PATH,
            target_database='sqlite',
            target_connection=DATABASE_PATH
        )
        
        pipeline = HealthcarePipeline(config)
        success = pipeline.run_pipeline()
        
        if success:
            flash("Pipeline completed successfully!", 'success')
        else:
            flash("Pipeline failed!", 'error')
        
        return redirect(url_for('pipeline'))
    except Exception as e:
        flash(f"Error running pipeline: {str(e)}", 'error')
        return redirect(url_for('pipeline'))

# API Endpoints
@app.route('/api/metrics')
def api_metrics():
    """API endpoint for key metrics"""
    try:
        patient_count = data_manager.get_patient_count()
        admission_count = data_manager.get_admission_count()
        financial_summary = data_manager.get_financial_summary()
        
        return jsonify({
            'patient_count': patient_count,
            'admission_count': admission_count,
            'financial_summary': financial_summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients')
def api_patients():
    """API endpoint for patients"""
    try:
        limit = request.args.get('limit', 100, type=int)
        conn = data_manager.get_database_connection()
        df = pd.read_sql_query("""
            SELECT 
                patient_id,
                first_name,
                last_name,
                date_of_birth,
                gender,
                insurance_type
            FROM patients
            LIMIT ?
        """, conn, params=[limit])
        conn.close()
        
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admissions')
def api_admissions():
    """API endpoint for admissions"""
    try:
        limit = request.args.get('limit', 100, type=int)
        conn = data_manager.get_database_connection()
        df = pd.read_sql_query("""
            SELECT 
                a.admission_id,
                p.first_name || ' ' || p.last_name as patient_name,
                a.admission_date,
                a.discharge_date,
                a.admission_type,
                a.department,
                a.attending_physician,
                a.length_of_stay,
                fd.total_charges,
                fd.net_revenue
            FROM admissions a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN financial_data fd ON a.admission_id = fd.admission_id
            ORDER BY a.admission_date DESC
            LIMIT ?
        """, conn, params=[limit])
        conn.close()
        
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/physicians')
def api_physicians():
    """API endpoint for physician performance"""
    try:
        limit = request.args.get('limit', 20, type=int)
        df = data_manager.get_physician_performance(limit)
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/departments')
def api_departments():
    """API endpoint for department metrics"""
    try:
        df = data_manager.get_department_metrics()
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quality')
def api_quality():
    """API endpoint for quality metrics"""
    try:
        df = data_manager.get_quality_metrics()
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/financial')
def api_financial():
    """API endpoint for financial performance"""
    try:
        df = data_manager.get_financial_performance()
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics')
def api_analytics():
    """API endpoint for analytics data"""
    try:
        # Get various analytics data
        top_diagnoses = data_manager.get_top_diagnoses(10)
        physician_performance = data_manager.get_physician_performance(10)
        department_metrics = data_manager.get_department_metrics()
        
        return jsonify({
            'top_diagnoses': top_diagnoses.to_dict('records'),
            'physician_performance': physician_performance.to_dict('records'),
            'department_metrics': department_metrics.to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_templates():
    """Create HTML templates for the web application"""
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    # Base template
    base_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Healthcare Analytics{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .sidebar { min-height: 100vh; background-color: #f8f9fa; }
        .main-content { padding: 20px; }
        .metric-card { border-left: 4px solid #007bff; }
        .metric-card.success { border-left-color: #28a745; }
        .metric-card.warning { border-left-color: #ffc107; }
        .metric-card.danger { border-left-color: #dc3545; }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <nav class="col-md-2 sidebar p-3">
                <h4 class="text-center mb-4">
                    <i class="fas fa-heartbeat text-primary"></i>
                    Healthcare Analytics
                </h4>
                <ul class="nav flex-column">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('dashboard') }}">
                            <i class="fas fa-tachometer-alt"></i> Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('analytics') }}">
                            <i class="fas fa-chart-line"></i> Analytics
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('patients') }}">
                            <i class="fas fa-users"></i> Patients
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('admissions') }}">
                            <i class="fas fa-hospital"></i> Admissions
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('pipeline') }}">
                            <i class="fas fa-cogs"></i> Pipeline
                        </a>
                    </li>
                </ul>
            </nav>
            
            <!-- Main Content -->
            <main class="col-md-10 main-content">
                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        {% for category, message in messages %}
                            <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                                {{ message }}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
                
                {% block content %}{% endblock %}
            </main>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
'''
    
    # Dashboard template
    dashboard_html = '''
{% extends "base.html" %}

{% block title %}Dashboard - Healthcare Analytics{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1><i class="fas fa-tachometer-alt"></i> Dashboard</h1>
    <div class="text-muted">Last updated: {{ moment().format('YYYY-MM-DD HH:mm:ss') }}</div>
</div>

{% if error %}
<div class="alert alert-danger">
    <i class="fas fa-exclamation-triangle"></i>
    Unable to load dashboard data. Please check the database connection.
</div>
{% else %}
<!-- Key Metrics -->
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card metric-card">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title text-muted">Total Patients</h6>
                        <h3 class="mb-0">{{ "{:,}".format(patient_count) }}</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-users fa-2x text-primary"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card metric-card">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title text-muted">Total Admissions</h6>
                        <h3 class="mb-0">{{ "{:,}".format(admission_count) }}</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-hospital fa-2x text-success"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card metric-card">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title text-muted">Total Revenue</h6>
                        <h3 class="mb-0">${{ "{:,.0f}".format(financial_summary.net_revenue) }}</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-dollar-sign fa-2x text-warning"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card metric-card">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title text-muted">Avg. Charge</h6>
                        <h3 class="mb-0">${{ "{:,.0f}".format(financial_summary.avg_charge) }}</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-chart-line fa-2x text-info"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Recent Admissions and Top Diagnoses -->
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-clock"></i> Recent Admissions</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Patient</th>
                                <th>Admission Date</th>
                                <th>Type</th>
                                <th>Physician</th>
                                <th>Revenue</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for admission in recent_admissions %}
                            <tr>
                                <td>{{ admission.patient_name }}</td>
                                <td>{{ admission.admission_date[:10] }}</td>
                                <td><span class="badge bg-primary">{{ admission.admission_type }}</span></td>
                                <td>{{ admission.attending_physician }}</td>
                                <td>${{ "{:,.0f}".format(admission.net_revenue) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-stethoscope"></i> Top Diagnoses</h5>
            </div>
            <div class="card-body">
                {% for diagnosis in top_diagnoses %}
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div>
                        <strong>{{ diagnosis.diagnosis_description }}</strong>
                        <br><small class="text-muted">{{ diagnosis.case_count }} cases</small>
                    </div>
                    <div class="text-end">
                        <div>${{ "{:,.0f}".format(diagnosis.avg_revenue) }}</div>
                        <small class="text-muted">{{ "%.1f"|format(diagnosis.avg_los) }} days avg</small>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>

<!-- Physician Performance -->
<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-user-md"></i> Top Performing Physicians</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Physician</th>
                                <th>Total Patients</th>
                                <th>Avg. Length of Stay</th>
                                <th>Avg. Satisfaction</th>
                                <th>Complication Rate</th>
                                <th>Avg. Revenue</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for physician in physician_performance %}
                            <tr>
                                <td>{{ physician.physician_name }}</td>
                                <td>{{ physician.total_patients }}</td>
                                <td>{{ "%.1f"|format(physician.avg_los) }} days</td>
                                <td>{{ "%.1f"|format(physician.avg_satisfaction) }}/5.0</td>
                                <td>{{ "%.1f"|format(physician.complication_rate * 100) }}%</td>
                                <td>${{ "{:,.0f}".format(physician.avg_revenue) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}
{% endblock %}
'''
    
    # Write templates
    with open(templates_dir / 'base.html', 'w') as f:
        f.write(base_html)
    
    with open(templates_dir / 'dashboard.html', 'w') as f:
        f.write(dashboard_html)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Healthcare Analytics Web Application')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', default=5000, type=int, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Create templates
    create_templates()
    
    print(f"Starting Healthcare Analytics Web Application on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop")
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
