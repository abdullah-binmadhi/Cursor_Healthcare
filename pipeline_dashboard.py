#!/usr/bin/env python3
"""
Healthcare Pipeline Dashboard
A web-based dashboard for monitoring the healthcare data pipeline
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os
import sys
from datetime import datetime, timedelta
import threading
import time
from pathlib import Path

# Import pipeline components
from healthcare_pipeline import HealthcarePipeline, PipelineConfig
from pipeline_scheduler import PipelineScheduler, PipelineMonitor

app = Flask(__name__)

# Global scheduler instance
scheduler = None
monitor = None

def initialize_scheduler():
    """Initialize the pipeline scheduler"""
    global scheduler, monitor
    
    config_file = 'pipeline_config.yaml'
    if os.path.exists(config_file):
        scheduler = PipelineScheduler(config_file)
        monitor = PipelineMonitor(scheduler)
    else:
        # Use default configuration
        scheduler = PipelineScheduler()
        monitor = PipelineMonitor(scheduler)

@app.route('/')
def dashboard():
    """Main dashboard page"""
    if scheduler is None:
        initialize_scheduler()
    
    # Get current status
    status = scheduler.get_pipeline_status()
    recent_jobs = scheduler.get_job_history(5)
    
    # Get health report
    health_report = monitor.generate_health_report()
    
    return render_template('dashboard.html', 
                         status=status, 
                         recent_jobs=recent_jobs,
                         health_report=health_report)

@app.route('/api/status')
def api_status():
    """API endpoint for pipeline status"""
    if scheduler is None:
        initialize_scheduler()
    
    status = scheduler.get_pipeline_status()
    return jsonify(status)

@app.route('/api/jobs')
def api_jobs():
    """API endpoint for job history"""
    if scheduler is None:
        initialize_scheduler()
    
    limit = request.args.get('limit', 10, type=int)
    jobs = scheduler.get_job_history(limit)
    return jsonify(jobs)

@app.route('/api/health')
def api_health():
    """API endpoint for system health"""
    if scheduler is None:
        initialize_scheduler()
    
    health_report = monitor.generate_health_report()
    return jsonify(health_report)

@app.route('/run-job', methods=['POST'])
def run_job():
    """Run a manual pipeline job"""
    if scheduler is None:
        initialize_scheduler()
    
    environment = request.form.get('environment', 'development')
    
    # Run job in background thread
    def run_background_job():
        scheduler.run_manual_job(environment)
    
    thread = threading.Thread(target=run_background_job)
    thread.start()
    
    return redirect(url_for('dashboard'))

@app.route('/logs')
def view_logs():
    """View pipeline logs"""
    log_files = []
    log_dir = Path('.')
    
    for log_file in log_dir.glob('*.log'):
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
                log_files.append({
                    'name': log_file.name,
                    'size': len(lines),
                    'last_modified': datetime.fromtimestamp(log_file.stat().st_mtime),
                    'last_lines': lines[-20:] if len(lines) > 20 else lines
                })
        except Exception as e:
            log_files.append({
                'name': log_file.name,
                'error': str(e)
            })
    
    return render_template('logs.html', log_files=log_files)

@app.route('/metrics')
def view_metrics():
    """View pipeline metrics"""
    metrics_files = []
    metrics_dir = Path('.')
    
    for metrics_file in metrics_dir.glob('*metrics*.json'):
        try:
            with open(metrics_file, 'r') as f:
                metrics = json.load(f)
                metrics_files.append({
                    'name': metrics_file.name,
                    'data': metrics,
                    'last_modified': datetime.fromtimestamp(metrics_file.stat().st_mtime)
                })
        except Exception as e:
            metrics_files.append({
                'name': metrics_file.name,
                'error': str(e)
            })
    
    return render_template('metrics.html', metrics_files=metrics_files)

@app.route('/config')
def view_config():
    """View pipeline configuration"""
    config_file = 'pipeline_config.yaml'
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config_content = f.read()
    else:
        config_content = "Configuration file not found"
    
    return render_template('config.html', config_content=config_content)

# Create templates directory and HTML templates
def create_templates():
    """Create HTML templates for the dashboard"""
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    # Dashboard template
    dashboard_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Healthcare Pipeline Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .status-card { margin-bottom: 20px; }
        .health-indicator { font-size: 24px; }
        .health-healthy { color: #28a745; }
        .health-warning { color: #ffc107; }
        .health-critical { color: #dc3545; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">Healthcare Pipeline Dashboard</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Dashboard</a>
                <a class="nav-link" href="/logs">Logs</a>
                <a class="nav-link" href="/metrics">Metrics</a>
                <a class="nav-link" href="/config">Config</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <!-- Pipeline Status -->
            <div class="col-md-6">
                <div class="card status-card">
                    <div class="card-header">
                        <h5>Pipeline Status</h5>
                    </div>
                    <div class="card-body">
                        <p><strong>Scheduler:</strong> 
                            <span class="badge bg-{{ 'success' if status.scheduler_running else 'danger' }}">
                                {{ 'Running' if status.scheduler_running else 'Stopped' }}
                            </span>
                        </p>
                        <p><strong>Total Jobs:</strong> {{ status.total_jobs }}</p>
                        <p><strong>Successful:</strong> {{ status.successful_jobs }}</p>
                        <p><strong>Failed:</strong> {{ status.failed_jobs }}</p>
                        
                        <form method="POST" action="/run-job" class="mt-3">
                            <div class="mb-3">
                                <label for="environment" class="form-label">Environment:</label>
                                <select name="environment" id="environment" class="form-select">
                                    <option value="development">Development</option>
                                    <option value="staging">Staging</option>
                                    <option value="production">Production</option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-primary">Run Manual Job</button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- System Health -->
            <div class="col-md-6">
                <div class="card status-card">
                    <div class="card-header">
                        <h5>System Health</h5>
                    </div>
                    <div class="card-body">
                        <div class="health-indicator health-{{ health_report.overall_health }}">
                            <strong>{{ health_report.overall_health.upper() }}</strong>
                        </div>
                        
                        {% if health_report.system_metrics %}
                        <p><strong>CPU:</strong> {{ "%.1f"|format(health_report.system_metrics.cpu_percent) }}%</p>
                        <p><strong>Memory:</strong> {{ "%.1f"|format(health_report.system_metrics.memory_percent) }}%</p>
                        <p><strong>Disk:</strong> {{ "%.1f"|format(health_report.system_metrics.disk_percent) }}%</p>
                        {% endif %}
                        
                        {% if health_report.database_health %}
                        <p><strong>Database:</strong> 
                            <span class="badge bg-{{ 'success' if health_report.database_health.status == 'healthy' else 'danger' }}">
                                {{ health_report.database_health.status }}
                            </span>
                        </p>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>

        <!-- Recent Jobs -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5>Recent Jobs</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Job ID</th>
                                        <th>Environment</th>
                                        <th>Status</th>
                                        <th>Start Time</th>
                                        <th>Duration</th>
                                        <th>Records Processed</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for job in recent_jobs %}
                                    <tr>
                                        <td>{{ job.job_id }}</td>
                                        <td>{{ job.environment }}</td>
                                        <td>
                                            <span class="badge bg-{{ 'success' if job.status == 'completed' else 'danger' }}">
                                                {{ job.status }}
                                            </span>
                                        </td>
                                        <td>{{ job.start_time.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                                        <td>{{ "%.2f"|format(job.processing_time) }}s</td>
                                        <td>{{ job.metrics.records_processed if job.metrics else 'N/A' }}</td>
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
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(function() {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
'''
    
    # Logs template
    logs_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pipeline Logs</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">Healthcare Pipeline Dashboard</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Dashboard</a>
                <a class="nav-link active" href="/logs">Logs</a>
                <a class="nav-link" href="/metrics">Metrics</a>
                <a class="nav-link" href="/config">Config</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h2>Pipeline Logs</h2>
        
        {% for log_file in log_files %}
        <div class="card mb-3">
            <div class="card-header">
                <h5>{{ log_file.name }}</h5>
                <small>Size: {{ log_file.size }} lines | Last modified: {{ log_file.last_modified.strftime('%Y-%m-%d %H:%M:%S') }}</small>
            </div>
            <div class="card-body">
                {% if log_file.last_lines %}
                <pre style="max-height: 300px; overflow-y: auto;">{% for line in log_file.last_lines %}{{ line }}{% endfor %}</pre>
                {% else %}
                <p class="text-muted">No log content available</p>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''
    
    # Metrics template
    metrics_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pipeline Metrics</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">Healthcare Pipeline Dashboard</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Dashboard</a>
                <a class="nav-link" href="/logs">Logs</a>
                <a class="nav-link active" href="/metrics">Metrics</a>
                <a class="nav-link" href="/config">Config</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h2>Pipeline Metrics</h2>
        
        {% for metrics_file in metrics_files %}
        <div class="card mb-3">
            <div class="card-header">
                <h5>{{ metrics_file.name }}</h5>
                <small>Last modified: {{ metrics_file.last_modified.strftime('%Y-%m-%d %H:%M:%S') }}</small>
            </div>
            <div class="card-body">
                <pre>{{ metrics_file.data | tojson(indent=2) }}</pre>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''
    
    # Config template
    config_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pipeline Configuration</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">Healthcare Pipeline Dashboard</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Dashboard</a>
                <a class="nav-link" href="/logs">Logs</a>
                <a class="nav-link" href="/metrics">Metrics</a>
                <a class="nav-link active" href="/config">Config</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h2>Pipeline Configuration</h2>
        
        <div class="card">
            <div class="card-body">
                <pre>{{ config_content }}</pre>
            </div>
        </div>
    </div>
</body>
</html>
'''
    
    # Write templates
    with open(templates_dir / 'dashboard.html', 'w') as f:
        f.write(dashboard_html)
    
    with open(templates_dir / 'logs.html', 'w') as f:
        f.write(logs_html)
    
    with open(templates_dir / 'metrics.html', 'w') as f:
        f.write(metrics_html)
    
    with open(templates_dir / 'config.html', 'w') as f:
        f.write(config_html)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Healthcare Pipeline Dashboard')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', default=5000, type=int, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Create templates
    create_templates()
    
    # Initialize scheduler
    initialize_scheduler()
    
    print(f"Starting Healthcare Pipeline Dashboard on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop")
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
