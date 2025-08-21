#!/usr/bin/env python3
"""
Quick Healthcare Dashboard
A simple dashboard that displays CSV data
"""

from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

def load_data():
    """Load CSV data"""
    try:
        df = pd.read_csv('healthcare_dataset.csv')
        return df
    except:
        return pd.DataFrame()

@app.route('/')
def dashboard():
    """Main dashboard"""
    df = load_data()
    
    if df.empty:
        return "No data found. Please check if healthcare_dataset.csv exists."
    
    # Calculate basic metrics
    total_patients = len(df)
    avg_age = round(df['Age'].mean(), 1) if 'Age' in df.columns else 0
    total_revenue = df['Billing Amount'].sum() if 'Billing Amount' in df.columns else 0
    avg_billing = round(df['Billing Amount'].mean(), 2) if 'Billing Amount' in df.columns else 0
    
    # Get recent data
    recent_data = df.head(10).to_dict('records')
    
    # Create HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Healthcare Analytics Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .metric-card { border-left: 4px solid #007bff; margin-bottom: 20px; }
            .metric-card.success { border-left-color: #28a745; }
            .metric-card.warning { border-left-color: #ffc107; }
        </style>
    </head>
    <body>
        <div class="container-fluid mt-4">
            <h1><i class="fas fa-heartbeat"></i> Healthcare Analytics Dashboard</h1>
            
            <!-- Key Metrics -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card metric-card">
                        <div class="card-body">
                            <h6 class="card-title text-muted">Total Patients</h6>
                            <h3 class="mb-0">{{ total_patients }}</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card metric-card success">
                        <div class="card-body">
                            <h6 class="card-title text-muted">Total Revenue</h6>
                            <h3 class="mb-0">${{ "{:,.0f}".format(total_revenue) }}</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card metric-card warning">
                        <div class="card-body">
                            <h6 class="card-title text-muted">Average Age</h6>
                            <h3 class="mb-0">{{ avg_age }} years</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card metric-card">
                        <div class="card-body">
                            <h6 class="card-title text-muted">Average Billing</h6>
                            <h3 class="mb-0">${{ "{:,.0f}".format(avg_billing) }}</h3>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Data Table -->
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5>Recent Patient Data</h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Age</th>
                                            <th>Gender</th>
                                            <th>Medical Condition</th>
                                            <th>Billing Amount</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for row in recent_data %}
                                        <tr>
                                            <td>{{ row.Name }}</td>
                                            <td>{{ row.Age }}</td>
                                            <td>{{ row.Gender }}</td>
                                            <td>{{ row.Medical Condition }}</td>
                                            <td>${{ "{:,.0f}".format(row['Billing Amount']) }}</td>
                                        </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    return render_template_string(html_template, 
                                total_patients=total_patients,
                                total_revenue=total_revenue,
                                avg_age=avg_age,
                                avg_billing=avg_billing,
                                recent_data=recent_data)

if __name__ == '__main__':
    print("Starting Quick Healthcare Dashboard on http://localhost:3000")
    print("Press Ctrl+C to stop")
    app.run(host='localhost', port=3000, debug=False)
