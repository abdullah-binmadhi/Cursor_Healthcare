#!/usr/bin/env python3
"""
Simple Healthcare Analytics Dashboard
A lightweight web application to display healthcare analytics from CSV files
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import json
import os
from pathlib import Path
import numpy as np
from datetime import datetime

app = Flask(__name__)

class SimpleDataManager:
    """Simple data manager for CSV files"""
    
    def __init__(self):
        self.csv_files = {
            'main': 'healthcare_dataset.csv',
            'enriched': 'healthcare_dataset_enriched.csv',
            'physician': 'physician_performance.csv',
            'department': 'department_metrics.csv',
            'quality': 'quality_metrics.csv',
            'financial': 'financial_performance.csv',
            'demographics': 'patient_demographics.csv'
        }
    
    def load_csv_data(self, filename):
        """Load CSV data safely"""
        try:
            if os.path.exists(filename):
                return pd.read_csv(filename)
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return pd.DataFrame()
    
    def get_main_metrics(self):
        """Get key metrics from main dataset"""
        df = self.load_csv_data(self.csv_files['main'])
        if df.empty:
            return {}
        
        return {
            'total_patients': int(len(df)),
            'total_admissions': int(len(df)),
            'avg_age': float(round(df['Age'].mean(), 1)) if 'Age' in df.columns else 0.0,
            'gender_distribution': df['Gender'].value_counts().to_dict() if 'Gender' in df.columns else {},
            'avg_billing': float(round(df['Billing Amount'].mean(), 2)) if 'Billing Amount' in df.columns else 0.0,
            'total_revenue': float(df['Billing Amount'].sum()) if 'Billing Amount' in df.columns else 0.0
        }
    
    def get_enriched_metrics(self):
        """Get metrics from enriched dataset"""
        df = self.load_csv_data(self.csv_files['enriched'])
        if df.empty:
            return {}
        
        metrics = {
            'total_records': int(len(df)),
            'departments': df['Department'].value_counts().to_dict() if 'Department' in df.columns else {},
            'admission_types': df['Admission Type'].value_counts().to_dict() if 'Admission Type' in df.columns else {},
            'avg_length_of_stay': float(round(df['Length of Stay'].mean(), 1)) if 'Length of Stay' in df.columns else 0.0,
            'avg_satisfaction': float(round(df['Satisfaction Score'].mean(), 1)) if 'Satisfaction Score' in df.columns else 0.0,
            'total_cost': float(df['Total Cost'].sum()) if 'Total Cost' in df.columns else 0.0
        }
        
        # Add insurance analysis
        if 'Insurance Provider' in df.columns:
            metrics['insurance_analysis'] = df['Insurance Provider'].value_counts().to_dict()
        
        return metrics
    
    def get_physician_data(self):
        """Get physician performance data"""
        df = self.load_csv_data(self.csv_files['physician'])
        if df.empty:
            return []
        
        # Aggregate by physician
        if 'physician_name' in df.columns:
            return df.groupby('physician_name').agg({
                'total_patients': 'sum',
                'avg_length_of_stay': 'mean',
                'avg_satisfaction_score': 'mean',
                'avg_revenue': 'mean'
            }).round(2).reset_index().to_dict('records')
        return []
    
    def get_department_data(self):
        """Get department metrics"""
        df = self.load_csv_data(self.csv_files['department'])
        if df.empty:
            return []
        
        # Aggregate by department
        if 'department_name' in df.columns:
            return df.groupby('department_name').agg({
                'total_admissions': 'sum',
                'avg_length_of_stay': 'mean',
                'avg_cost': 'mean',
                'total_revenue': 'sum',
                'occupancy_rate': 'mean'
            }).round(2).reset_index().to_dict('records')
        return []
    
    def get_quality_data(self):
        """Get quality metrics"""
        df = self.load_csv_data(self.csv_files['quality'])
        if df.empty:
            return []
        
        return df.to_dict('records')
    
    def get_financial_data(self):
        """Get financial performance"""
        df = self.load_csv_data(self.csv_files['financial'])
        if df.empty:
            return []
        
        return df.to_dict('records')
    
    def get_recent_admissions(self, limit=10):
        """Get recent admissions"""
        df = self.load_csv_data(self.csv_files['main'])
        if df.empty:
            return []
        
        # Sort by date if available
        if 'Date of Admission' in df.columns:
            df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce')
            df = df.sort_values('Date of Admission', ascending=False)
        
        # Convert to records and handle column names with spaces
        records = df.head(limit).to_dict('records')
        for record in records:
            # Convert numpy types to Python types for JSON serialization
            for key, value in record.items():
                if hasattr(value, 'item'):
                    record[key] = value.item()
                elif pd.isna(value):
                    record[key] = None
        
        return records

# Initialize data manager
data_manager = SimpleDataManager()

@app.route('/')
def dashboard():
    """Main dashboard"""
    main_metrics = data_manager.get_main_metrics()
    enriched_metrics = data_manager.get_enriched_metrics()
    recent_admissions = data_manager.get_recent_admissions(10)
    
    return render_template('simple_dashboard.html',
                         main_metrics=main_metrics,
                         enriched_metrics=enriched_metrics,
                         recent_admissions=recent_admissions)

@app.route('/physicians')
def physicians():
    """Physician performance page"""
    physician_data = data_manager.get_physician_data()
    return render_template('physicians.html', physicians=physician_data)

@app.route('/departments')
def departments():
    """Department metrics page"""
    department_data = data_manager.get_department_data()
    return render_template('departments.html', departments=department_data)

@app.route('/quality')
def quality():
    """Quality metrics page"""
    quality_data = data_manager.get_quality_data()
    return render_template('quality.html', quality_metrics=quality_data)

@app.route('/financial')
def financial():
    """Financial performance page"""
    financial_data = data_manager.get_financial_data()
    return render_template('financial.html', financial_data=financial_data)

@app.route('/api/metrics')
def api_metrics():
    """API endpoint for metrics"""
    main_metrics = data_manager.get_main_metrics()
    enriched_metrics = data_manager.get_enriched_metrics()
    
    return jsonify({
        'main_metrics': main_metrics,
        'enriched_metrics': enriched_metrics
    })

@app.route('/api/physicians')
def api_physicians():
    """API endpoint for physician data"""
    physician_data = data_manager.get_physician_data()
    return jsonify(physician_data)

@app.route('/api/departments')
def api_departments():
    """API endpoint for department data"""
    department_data = data_manager.get_department_data()
    return jsonify(department_data)

def create_simple_templates():
    """Create simple HTML templates"""
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
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .metric-card { border-left: 4px solid #007bff; margin-bottom: 20px; }
        .metric-card.success { border-left-color: #28a745; }
        .metric-card.warning { border-left-color: #ffc107; }
        .metric-card.danger { border-left-color: #dc3545; }
        .chart-container { position: relative; height: 400px; margin: 20px 0; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="fas fa-heartbeat"></i> Healthcare Analytics
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Dashboard</a>
                <a class="nav-link" href="/physicians">Physicians</a>
                <a class="nav-link" href="/departments">Departments</a>
                <a class="nav-link" href="/quality">Quality</a>
                <a class="nav-link" href="/financial">Financial</a>
            </div>
        </div>
    </nav>

    <div class="container-fluid mt-4">
        {% block content %}{% endblock %}
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
<div class="row">
    <div class="col-12">
        <h1><i class="fas fa-tachometer-alt"></i> Healthcare Analytics Dashboard</h1>
        <p class="text-muted">Real-time analytics from healthcare data</p>
    </div>
</div>

<!-- Key Metrics -->
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card metric-card">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title text-muted">Total Patients</h6>
                        <h3 class="mb-0">{{ "{:,}".format(main_metrics.total_patients) }}</h3>
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
                        <h6 class="card-title text-muted">Total Revenue</h6>
                        <h3 class="mb-0">${{ "{:,.0f}".format(main_metrics.total_revenue) }}</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-dollar-sign fa-2x text-success"></i>
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
                        <h6 class="card-title text-muted">Avg. Age</h6>
                        <h3 class="mb-0">{{ main_metrics.avg_age }} years</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-user fa-2x text-warning"></i>
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
                        <h6 class="card-title text-muted">Avg. Billing</h6>
                        <h3 class="mb-0">${{ "{:,.0f}".format(main_metrics.avg_billing) }}</h3>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-chart-line fa-2x text-info"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Charts Row -->
<div class="row">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-pie"></i> Gender Distribution</h5>
            </div>
            <div class="card-body">
                <div class="chart-container">
                    <canvas id="genderChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-bar"></i> Department Distribution</h5>
            </div>
            <div class="card-body">
                <div class="chart-container">
                    <canvas id="departmentChart"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Recent Admissions -->
<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-clock"></i> Recent Admissions</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Patient Name</th>
                                <th>Age</th>
                                <th>Gender</th>
                                <th>Medical Condition</th>
                                <th>Admission Date</th>
                                <th>Billing Amount</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for admission in recent_admissions %}
                            <tr>
                                <td>{{ admission['Name'] }}</td>
                                <td>{{ admission['Age'] }}</td>
                                <td>{{ admission['Gender'] }}</td>
                                <td>{{ admission['Medical Condition'] }}</td>
                                <td>{{ admission['Date of Admission'] }}</td>
                                <td>${{ "{:,.0f}".format(admission['Billing Amount']) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
// Gender Distribution Chart
const genderData = {{ main_metrics.gender_distribution | tojson }};
const genderCtx = document.getElementById('genderChart').getContext('2d');
new Chart(genderCtx, {
    type: 'pie',
    data: {
        labels: Object.keys(genderData),
        datasets: [{
            data: Object.values(genderData),
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

// Department Distribution Chart
const deptData = {{ enriched_metrics.departments | tojson }};
const deptCtx = document.getElementById('departmentChart').getContext('2d');
new Chart(deptCtx, {
    type: 'bar',
    data: {
        labels: Object.keys(deptData),
        datasets: [{
            label: 'Admissions',
            data: Object.values(deptData),
            backgroundColor: '#36A2EB'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
</script>
{% endblock %}
'''
    
    # Physicians template
    physicians_html = '''
{% extends "base.html" %}

{% block title %}Physicians - Healthcare Analytics{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1><i class="fas fa-user-md"></i> Physician Performance</h1>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-line"></i> Physician Performance Metrics</h5>
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
                                <th>Avg. Revenue</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for physician in physicians %}
                            <tr>
                                <td>{{ physician.physician_name }}</td>
                                <td>{{ physician.total_patients }}</td>
                                <td>{{ physician.avg_length_of_stay }} days</td>
                                <td>{{ physician.avg_satisfaction_score }}/5.0</td>
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
{% endblock %}
'''
    
    # Departments template
    departments_html = '''
{% extends "base.html" %}

{% block title %}Departments - Healthcare Analytics{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1><i class="fas fa-building"></i> Department Performance</h1>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-bar"></i> Department Metrics</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Department</th>
                                <th>Total Admissions</th>
                                <th>Avg. Length of Stay</th>
                                <th>Avg. Cost</th>
                                <th>Total Revenue</th>
                                <th>Occupancy Rate</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for dept in departments %}
                            <tr>
                                <td>{{ dept.department_name }}</td>
                                <td>{{ "{:,}".format(dept.total_admissions) }}</td>
                                <td>{{ dept.avg_length_of_stay }} days</td>
                                <td>${{ "{:,.0f}".format(dept.avg_cost) }}</td>
                                <td>${{ "{:,.0f}".format(dept.total_revenue) }}</td>
                                <td>{{ "%.1f"|format(dept.occupancy_rate * 100) }}%</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
    
    # Quality template
    quality_html = '''
{% extends "base.html" %}

{% block title %}Quality - Healthcare Analytics{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1><i class="fas fa-shield-alt"></i> Quality Metrics</h1>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-area"></i> Quality Indicators</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Month/Year</th>
                                <th>HAI</th>
                                <th>Pressure Ulcers</th>
                                <th>Falls</th>
                                <th>Med Errors</th>
                                <th>Patient Satisfaction</th>
                                <th>Readmission Rate</th>
                                <th>Mortality Rate</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for metric in quality_metrics %}
                            <tr>
                                <td>{{ metric.month }}/{{ metric.year }}</td>
                                <td>{{ metric.hospital_acquired_infections }}</td>
                                <td>{{ metric.pressure_ulcers }}</td>
                                <td>{{ metric.falls }}</td>
                                <td>{{ metric.medication_errors }}</td>
                                <td>{{ "%.1f"|format(metric.patient_satisfaction_avg) }}/5.0</td>
                                <td>{{ "%.1f"|format(metric.readmission_rate * 100) }}%</td>
                                <td>{{ "%.1f"|format(metric.mortality_rate * 100) }}%</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
    
    # Financial template
    financial_html = '''
{% extends "base.html" %}

{% block title %}Financial - Healthcare Analytics{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1><i class="fas fa-dollar-sign"></i> Financial Performance</h1>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-line"></i> Financial Metrics</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Month/Year</th>
                                <th>Total Revenue</th>
                                <th>Total Expenses</th>
                                <th>Net Income</th>
                                <th>Operating Margin</th>
                                <th>Bad Debt</th>
                                <th>Charity Care</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for financial in financial_data %}
                            <tr>
                                <td>{{ financial.month }}/{{ financial.year }}</td>
                                <td>${{ "{:,.0f}".format(financial.total_revenue) }}</td>
                                <td>${{ "{:,.0f}".format(financial.total_expenses) }}</td>
                                <td class="{{ 'text-success' if financial.net_income > 0 else 'text-danger' }}">
                                    ${{ "{:,.0f}".format(financial.net_income) }}
                                </td>
                                <td>{{ "%.1f"|format(financial.operating_margin * 100) }}%</td>
                                <td>${{ "{:,.0f}".format(financial.bad_debt) }}</td>
                                <td>${{ "{:,.0f}".format(financial.charity_care) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''
    
    # Write templates
    with open(templates_dir / 'simple_dashboard.html', 'w') as f:
        f.write(dashboard_html)
    
    with open(templates_dir / 'physicians.html', 'w') as f:
        f.write(physicians_html)
    
    with open(templates_dir / 'departments.html', 'w') as f:
        f.write(departments_html)
    
    with open(templates_dir / 'quality.html', 'w') as f:
        f.write(quality_html)
    
    with open(templates_dir / 'financial.html', 'w') as f:
        f.write(financial_html)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple Healthcare Analytics Dashboard')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', default=5000, type=int, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Create templates
    create_simple_templates()
    
    print(f"Starting Simple Healthcare Analytics Dashboard on http://{args.host}:{args.port}")
    print("Available CSV files:")
    for name, filename in data_manager.csv_files.items():
        if os.path.exists(filename):
            print(f"  ✓ {name}: {filename}")
        else:
            print(f"  ✗ {name}: {filename} (not found)")
    print("\nPress Ctrl+C to stop")
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
