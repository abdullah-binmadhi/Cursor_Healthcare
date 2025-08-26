#!/usr/bin/env python3
"""
Healthcare Pipeline Scheduler
Schedules and monitors the healthcare data pipeline with alerting and reporting
"""

import schedule
import time
import yaml
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import threading
import subprocess
import psutil
import requests

# Import the pipeline
from healthcare_pipeline import HealthcarePipeline, PipelineConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PipelineScheduler:
    """Scheduler for healthcare data pipeline"""
    
    def __init__(self, config_file: str = 'pipeline_config.yaml'):
        self.config_file = config_file
        self.config = self.load_config()
        self.pipeline_history = []
        self.current_job = None
        self.is_running = False
        
    def load_config(self) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {self.config_file}")
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            return {}
    
    def create_pipeline_config(self, environment: str = 'development') -> PipelineConfig:
        """Create pipeline configuration from YAML config"""
        env_config = self.config.get('environments', {}).get(environment, {})
        
        return PipelineConfig(
            source_type=self.config.get('source', {}).get('type', 'csv'),
            source_path=self.config.get('source', {}).get('path', 'healthcare_dataset.csv'),
            target_database=env_config.get('target', {}).get('database', 'sqlite'),
            target_connection=env_config.get('target', {}).get('connection', 'healthcare_analytics.db'),
            batch_size=self.config.get('processing', {}).get('batch_size', 1000),
            validation_enabled=self.config.get('processing', {}).get('validation', {}).get('enabled', True),
            backup_enabled=self.config.get('backup', {}).get('enabled', True),
            monitoring_enabled=self.config.get('monitoring', {}).get('enabled', True),
            schedule_interval=self.config.get('scheduling', {}).get('interval', 'daily')
        )
    
    def run_pipeline_job(self, environment: str = 'development') -> Dict:
        """Run a single pipeline job"""
        job_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        job_info = {
            'job_id': job_id,
            'environment': environment,
            'start_time': datetime.now(),
            'status': 'running',
            'config': self.create_pipeline_config(environment)
        }
        
        logger.info(f"Starting pipeline job {job_id} for environment {environment}")
        
        try:
            # Create and run pipeline
            pipeline = HealthcarePipeline(job_info['config'])
            success = pipeline.run_pipeline()
            
            job_info['end_time'] = datetime.now()
            job_info['status'] = 'completed' if success else 'failed'
            job_info['processing_time'] = (
                job_info['end_time'] - job_info['start_time']
            ).total_seconds()
            
            # Get pipeline metrics
            if hasattr(pipeline, 'monitor'):
                job_info['metrics'] = pipeline.monitor.get_summary()
            
            # Send alerts if needed
            if self.config.get('monitoring', {}).get('alerts', {}).get('enabled', False):
                self.send_alert(job_info)
            
            logger.info(f"Pipeline job {job_id} completed with status: {job_info['status']}")
            
        except Exception as e:
            job_info['end_time'] = datetime.now()
            job_info['status'] = 'error'
            job_info['error'] = str(e)
            job_info['processing_time'] = (
                job_info['end_time'] - job_info['start_time']
            ).total_seconds()
            
            logger.error(f"Pipeline job {job_id} failed: {str(e)}")
            
            # Send error alert
            if self.config.get('monitoring', {}).get('alerts', {}).get('enabled', False):
                self.send_alert(job_info)
        
        # Store job history
        self.pipeline_history.append(job_info)
        
        # Keep only last 100 jobs
        if len(self.pipeline_history) > 100:
            self.pipeline_history = self.pipeline_history[-100:]
        
        return job_info
    
    def send_alert(self, job_info: Dict):
        """Send email alert based on job status"""
        try:
            alert_config = self.config.get('monitoring', {}).get('alerts', {})
            email_config = alert_config.get('email', {})
            
            if not email_config.get('enabled', False):
                return
            
            # Check if alert is needed
            if not self.should_send_alert(job_info):
                return
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = email_config.get('username')
            msg['To'] = ', '.join(email_config.get('recipients', []))
            msg['Subject'] = f"Healthcare Pipeline Alert - {job_info['status'].upper()}"
            
            # Create email body
            body = self.create_alert_message(job_info)
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(email_config.get('smtp_server'), email_config.get('smtp_port'))
            server.starttls()
            server.login(email_config.get('username'), email_config.get('password'))
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Alert sent for job {job_info['job_id']}")
            
        except Exception as e:
            logger.error(f"Failed to send alert: {str(e)}")
    
    def should_send_alert(self, job_info: Dict) -> bool:
        """Determine if an alert should be sent"""
        alert_config = self.config.get('monitoring', {}).get('alerts', {})
        conditions = alert_config.get('conditions', {})
        
        # Alert on failure
        if job_info['status'] in ['failed', 'error']:
            return True
        
        # Alert on slow processing
        processing_time = job_info.get('processing_time', 0)
        threshold = conditions.get('processing_time_threshold', 300)
        if processing_time > threshold:
            return True
        
        # Alert on high error rate
        metrics = job_info.get('metrics', {})
        error_rate = 100 - metrics.get('success_rate', 100)
        error_threshold = conditions.get('error_rate_threshold', 5.0)
        if error_rate > error_threshold:
            return True
        
        return False
    
    def create_alert_message(self, job_info: Dict) -> str:
        """Create alert message content"""
        message = f"""
Healthcare Pipeline Alert

Job ID: {job_info['job_id']}
Environment: {job_info['environment']}
Status: {job_info['status'].upper()}
Start Time: {job_info['start_time']}
End Time: {job_info['end_time']}
Processing Time: {job_info.get('processing_time', 0):.2f} seconds

"""
        
        if 'metrics' in job_info:
            metrics = job_info['metrics']
            message += f"""
Metrics:
- Records Processed: {metrics.get('records_processed', 0):,}
- Records Failed: {metrics.get('records_failed', 0):,}
- Success Rate: {metrics.get('success_rate', 0):.1f}%
- Validation Errors: {metrics.get('validation_errors', 0)}
"""
        
        if 'error' in job_info:
            message += f"\nError: {job_info['error']}\n"
        
        message += f"""
This is an automated alert from the Healthcare Data Pipeline.
Please check the logs for more details.
"""
        
        return message
    
    def setup_schedule(self):
        """Setup pipeline schedule based on configuration"""
        schedule_config = self.config.get('scheduling', {})
        
        if not schedule_config.get('enabled', False):
            logger.info("Scheduling is disabled")
            return
        
        interval = schedule_config.get('interval', 'daily')
        start_time = schedule_config.get('start_time', '01:00')
        
        if interval == 'hourly':
            schedule.every().hour.at(start_time).do(self.run_pipeline_job)
        elif interval == 'daily':
            schedule.every().day.at(start_time).do(self.run_pipeline_job)
        elif interval == 'weekly':
            schedule.every().monday.at(start_time).do(self.run_pipeline_job)
        elif interval == 'monthly':
            schedule.every().month.at(start_time).do(self.run_pipeline_job)
        
        logger.info(f"Pipeline scheduled to run {interval} at {start_time}")
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        self.is_running = True
        logger.info("Pipeline scheduler started")
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.is_running = False
        logger.info("Pipeline scheduler stopped")
    
    def get_pipeline_status(self) -> Dict:
        """Get current pipeline status"""
        return {
            'scheduler_running': self.is_running,
            'current_job': self.current_job,
            'total_jobs': len(self.pipeline_history),
            'successful_jobs': len([j for j in self.pipeline_history if j['status'] == 'completed']),
            'failed_jobs': len([j for j in self.pipeline_history if j['status'] in ['failed', 'error']]),
            'last_job': self.pipeline_history[-1] if self.pipeline_history else None
        }
    
    def get_job_history(self, limit: int = 10) -> List[Dict]:
        """Get recent job history"""
        return self.pipeline_history[-limit:] if self.pipeline_history else []
    
    def run_manual_job(self, environment: str = 'development') -> Dict:
        """Run a manual pipeline job"""
        logger.info(f"Running manual pipeline job for environment: {environment}")
        return self.run_pipeline_job(environment)

class PipelineMonitor:
    """Monitor pipeline performance and health"""
    
    def __init__(self, scheduler: PipelineScheduler):
        self.scheduler = scheduler
        self.monitoring_data = []
    
    def collect_system_metrics(self) -> Dict:
        """Collect system performance metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'timestamp': datetime.now(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available,
                'disk_percent': disk.percent,
                'disk_free': disk.free
            }
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
            return {}
    
    def check_database_health(self) -> Dict:
        """Check database connectivity and health"""
        try:
            # Try to connect to the database
            config = self.scheduler.create_pipeline_config()
            
            if config.target_database == 'sqlite':
                import sqlite3
                conn = sqlite3.connect(config.target_connection)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM patients")
                patient_count = cursor.fetchone()[0]
                conn.close()
                
                return {
                    'status': 'healthy',
                    'patient_count': patient_count,
                    'connection_type': 'sqlite'
                }
            
            elif config.target_database == 'postgresql':
                # Add PostgreSQL health check
                return {
                    'status': 'healthy',
                    'connection_type': 'postgresql'
                }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'connection_type': config.target_database
            }
    
    def generate_health_report(self) -> Dict:
        """Generate comprehensive health report"""
        system_metrics = self.collect_system_metrics()
        database_health = self.check_database_health()
        pipeline_status = self.scheduler.get_pipeline_status()
        
        return {
            'timestamp': datetime.now(),
            'system_metrics': system_metrics,
            'database_health': database_health,
            'pipeline_status': pipeline_status,
            'overall_health': self.calculate_overall_health(
                system_metrics, database_health, pipeline_status
            )
        }
    
    def calculate_overall_health(self, system_metrics: Dict, database_health: Dict, pipeline_status: Dict) -> str:
        """Calculate overall system health"""
        health_score = 100
        
        # System health (30% weight)
        if system_metrics:
            if system_metrics.get('cpu_percent', 0) > 80:
                health_score -= 10
            if system_metrics.get('memory_percent', 0) > 90:
                health_score -= 10
            if system_metrics.get('disk_percent', 0) > 90:
                health_score -= 10
        
        # Database health (40% weight)
        if database_health.get('status') != 'healthy':
            health_score -= 40
        
        # Pipeline health (30% weight)
        if pipeline_status.get('failed_jobs', 0) > 0:
            health_score -= 15
        if not pipeline_status.get('scheduler_running', False):
            health_score -= 15
        
        if health_score >= 80:
            return 'healthy'
        elif health_score >= 60:
            return 'warning'
        else:
            return 'critical'
    
    def save_health_report(self, report: Dict, filename: str = None):
        """Save health report to file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'health_report_{timestamp}.json'
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, default=str, indent=2)
            logger.info(f"Health report saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving health report: {str(e)}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Healthcare Pipeline Scheduler')
    parser.add_argument('--config', default='pipeline_config.yaml', help='Configuration file')
    parser.add_argument('--environment', default='development', help='Environment to run')
    parser.add_argument('--manual', action='store_true', help='Run manual job')
    parser.add_argument('--monitor', action='store_true', help='Run monitoring only')
    parser.add_argument('--schedule', action='store_true', help='Run scheduler')
    
    args = parser.parse_args()
    
    # Create scheduler
    scheduler = PipelineScheduler(args.config)
    monitor = PipelineMonitor(scheduler)
    
    if args.manual:
        # Run manual job
        job_result = scheduler.run_manual_job(args.environment)
        print(f"Manual job completed: {job_result['status']}")
        
    elif args.monitor:
        # Run monitoring
        report = monitor.generate_health_report()
        monitor.save_health_report(report)
        print(f"Health report generated: {report['overall_health']}")
        
    elif args.schedule:
        # Run scheduler
        scheduler.setup_schedule()
        try:
            scheduler.run_scheduler()
        except KeyboardInterrupt:
            scheduler.stop_scheduler()
            print("Scheduler stopped by user")
    
    else:
        # Default: run manual job
        job_result = scheduler.run_manual_job(args.environment)
        print(f"Pipeline job completed: {job_result['status']}")

if __name__ == "__main__":
    main()
