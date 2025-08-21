# Healthcare Data Pipeline

A comprehensive ETL (Extract, Transform, Load) pipeline for healthcare analytics with data validation, monitoring, scheduling, and web dashboard.

## 🚀 Features

### Core Pipeline
- **Data Extraction**: Support for CSV, API, and database sources
- **Data Validation**: Comprehensive data quality checks and validation rules
- **Data Transformation**: Cleaning, standardization, and enrichment
- **Data Loading**: Support for SQLite and PostgreSQL databases
- **Error Handling**: Robust error handling and recovery mechanisms

### Monitoring & Scheduling
- **Pipeline Scheduler**: Automated job scheduling (hourly, daily, weekly, monthly)
- **Health Monitoring**: System performance and database health checks
- **Alerting**: Email notifications for failures and performance issues
- **Web Dashboard**: Real-time monitoring interface
- **Metrics Collection**: Detailed performance and quality metrics

### Data Quality
- **Validation Rules**: Configurable validation for patient, admission, and financial data
- **Data Cleaning**: Automatic cleaning and standardization
- **Outlier Detection**: Statistical outlier detection and handling
- **Duplicate Detection**: Identification and handling of duplicate records

## 📁 Project Structure

```
healthcare-pipeline/
├── healthcare_pipeline.py          # Main ETL pipeline
├── pipeline_scheduler.py           # Job scheduler and monitoring
├── pipeline_dashboard.py           # Web dashboard
├── pipeline_config.yaml            # Configuration file
├── requirements.txt                # Python dependencies
├── healthcare_dataset.csv          # Sample data
├── backups/                        # Database backups
├── logs/                          # Pipeline logs
└── templates/                     # Dashboard templates
```

## 🛠️ Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Configuration
Copy and modify the configuration file:
```bash
cp pipeline_config.yaml my_config.yaml
# Edit my_config.yaml with your settings
```

### 3. Prepare Data
Ensure your healthcare dataset is available:
```bash
# Your CSV file should have columns like:
# Name, Age, Gender, Date of Admission, Discharge Date, Admission Type, 
# Doctor, Hospital, Insurance Provider, Billing Amount, Room Number, 
# Medical Condition, Medication, Test Results
```

## 🚀 Quick Start

### 1. Run Single Pipeline Job
```bash
# Run with default configuration
python healthcare_pipeline.py

# Run with custom configuration
python healthcare_pipeline.py --config my_config.yaml
```

### 2. Start the Scheduler
```bash
# Run scheduled jobs
python pipeline_scheduler.py --schedule

# Run manual job
python pipeline_scheduler.py --manual

# Run monitoring only
python pipeline_scheduler.py --monitor
```

### 3. Start the Web Dashboard
```bash
# Start dashboard on default port 5000
python pipeline_dashboard.py

# Start on custom host and port
python pipeline_dashboard.py --host 0.0.0.0 --port 8080

# Enable debug mode
python pipeline_dashboard.py --debug
```

## 📊 Configuration

### Pipeline Configuration (pipeline_config.yaml)

```yaml
# Data Source Configuration
source:
  type: "csv"  # csv, api, database
  path: "healthcare_dataset.csv"
  
# Target Database Configuration
target:
  database: "sqlite"  # sqlite, postgresql
  connection: "healthcare_analytics.db"
  
# Processing Configuration
processing:
  batch_size: 1000
  validation:
    enabled: true
    strict_mode: false
    
# Monitoring Configuration
monitoring:
  enabled: true
  log_level: "INFO"
  alerts:
    enabled: true
    email:
      smtp_server: "smtp.gmail.com"
      recipients: ["admin@healthcare.com"]
      
# Scheduling Configuration
scheduling:
  enabled: true
  interval: "daily"  # hourly, daily, weekly, monthly
  start_time: "01:00"
```

### Environment-Specific Configurations

```yaml
environments:
  development:
    target:
      database: "sqlite"
      connection: "healthcare_dev.db"
    monitoring:
      log_level: "DEBUG"
      
  production:
    target:
      database: "postgresql"
      postgresql:
        host: "prod-db.healthcare.com"
        database: "healthcare_production"
    monitoring:
      log_level: "WARNING"
      alerts:
        enabled: true
```

## 🔧 Usage Examples

### 1. Basic Pipeline Execution

```python
from healthcare_pipeline import HealthcarePipeline, PipelineConfig

# Create configuration
config = PipelineConfig(
    source_type='csv',
    source_path='healthcare_dataset.csv',
    target_database='sqlite',
    target_connection='healthcare_analytics.db',
    validation_enabled=True,
    backup_enabled=True
)

# Run pipeline
pipeline = HealthcarePipeline(config)
success = pipeline.run_pipeline()

if success:
    print("Pipeline completed successfully!")
else:
    print("Pipeline failed!")
```

### 2. Custom Data Validation

```python
from healthcare_pipeline import DataValidator

# Validate patient data
df = pd.read_csv('healthcare_dataset.csv')
is_valid, errors = DataValidator.validate_patient_data(df)

if not is_valid:
    print("Validation errors:", errors)
```

### 3. Custom Data Transformation

```python
from healthcare_pipeline import DataTransformer

# Clean patient data
df_clean = DataTransformer.clean_patient_data(df)
df_clean = DataTransformer.clean_admission_data(df_clean)
df_clean = DataTransformer.clean_financial_data(df_clean)
```

### 4. Pipeline Monitoring

```python
from pipeline_scheduler import PipelineScheduler, PipelineMonitor

# Create scheduler
scheduler = PipelineScheduler('pipeline_config.yaml')
monitor = PipelineMonitor(scheduler)

# Get health report
health_report = monitor.generate_health_report()
print(f"System health: {health_report['overall_health']}")

# Get pipeline status
status = scheduler.get_pipeline_status()
print(f"Total jobs: {status['total_jobs']}")
```

## 📈 Monitoring & Dashboard

### Web Dashboard Features
- **Real-time Status**: Pipeline status and job history
- **System Health**: CPU, memory, disk usage monitoring
- **Job Management**: Manual job execution and scheduling
- **Logs Viewer**: Real-time log viewing and analysis
- **Metrics Display**: Performance metrics and data quality reports
- **Configuration Viewer**: Current pipeline configuration

### Dashboard Access
1. Start the dashboard: `python pipeline_dashboard.py`
2. Open browser: `http://localhost:5000`
3. Navigate through different sections:
   - **Dashboard**: Overview and status
   - **Logs**: Pipeline execution logs
   - **Metrics**: Performance and quality metrics
   - **Config**: Current configuration

### API Endpoints
```bash
# Get pipeline status
curl http://localhost:5000/api/status

# Get job history
curl http://localhost:5000/api/jobs?limit=10

# Get system health
curl http://localhost:5000/api/health
```

## 🔍 Data Validation Rules

### Patient Data Validation
- Required columns: Name, Age, Gender, Insurance Provider
- Age range: 0-120 years
- Valid genders: Male, Female, M, F
- Duplicate name detection

### Admission Data Validation
- Required columns: Date of Admission, Discharge Date, Admission Type
- Date range validation (no future dates)
- Discharge date must be after admission date
- Valid admission types: Emergency, Elective, Urgent, Transfer

### Financial Data Validation
- Required columns: Billing Amount
- No negative amounts
- Outlier detection (beyond 3 standard deviations)
- Amount range validation

## 📊 Metrics & Reporting

### Pipeline Metrics
- **Processing Time**: Total time for data processing
- **Records Processed**: Number of records successfully processed
- **Records Failed**: Number of records that failed validation
- **Success Rate**: Percentage of successful records
- **Validation Errors**: Number and types of validation errors

### System Metrics
- **CPU Usage**: System CPU utilization
- **Memory Usage**: System memory utilization
- **Disk Usage**: Available disk space
- **Database Health**: Database connectivity and performance

### Quality Metrics
- **Data Completeness**: Percentage of required fields populated
- **Data Accuracy**: Validation rule compliance
- **Data Consistency**: Format and value consistency
- **Data Timeliness**: Age of data and processing delays

## 🚨 Alerting & Notifications

### Alert Conditions
- **Pipeline Failures**: Job execution failures
- **Slow Processing**: Processing time exceeds threshold
- **High Error Rates**: Data quality below threshold
- **System Issues**: High CPU/memory usage

### Email Alerts
Configure email alerts in `pipeline_config.yaml`:
```yaml
monitoring:
  alerts:
    enabled: true
    email:
      smtp_server: "smtp.gmail.com"
      smtp_port: 587
      username: "${EMAIL_USER}"
      password: "${EMAIL_PASSWORD}"
      recipients: ["admin@healthcare.com"]
```

## 🔄 Scheduling

### Schedule Types
- **Hourly**: Run every hour at specified time
- **Daily**: Run once per day at specified time
- **Weekly**: Run once per week on specified day
- **Monthly**: Run once per month on specified date

### Schedule Configuration
```yaml
scheduling:
  enabled: true
  interval: "daily"
  start_time: "01:00"
  timezone: "UTC"
  options:
    retry_on_failure: true
    max_retries: 3
    retry_delay: 300
```

## 🛡️ Security & Backup

### Data Security
- **Encryption**: Optional data encryption (AES-256)
- **Access Control**: User-based access control
- **Audit Logging**: Comprehensive audit trails

### Backup Configuration
```yaml
backup:
  enabled: true
  directory: "backups"
  retention_days: 30
  compression: true
  schedule:
    frequency: "daily"
    time: "02:00"
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check database configuration
   python -c "import sqlite3; sqlite3.connect('healthcare_analytics.db')"
   ```

2. **Validation Errors**
   ```bash
   # Check data format
   head -5 healthcare_dataset.csv
   ```

3. **Pipeline Timeout**
   ```bash
   # Increase timeout in configuration
   processing:
     timeout: 600  # 10 minutes
   ```

4. **Memory Issues**
   ```bash
   # Reduce batch size
   processing:
     batch_size: 500
   ```

### Log Files
- `healthcare_pipeline.log`: Main pipeline logs
- `pipeline_scheduler.log`: Scheduler and monitoring logs
- `pipeline_metrics.json`: Performance metrics

### Debug Mode
```bash
# Enable debug logging
python healthcare_pipeline.py --debug

# Start dashboard in debug mode
python pipeline_dashboard.py --debug
```

## 📚 API Reference

### HealthcarePipeline Class
```python
class HealthcarePipeline:
    def __init__(self, config: PipelineConfig)
    def extract_data(self) -> pd.DataFrame
    def validate_data(self, df: pd.DataFrame) -> bool
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame
    def load_data(self, df: pd.DataFrame) -> bool
    def run_pipeline(self) -> bool
```

### PipelineScheduler Class
```python
class PipelineScheduler:
    def __init__(self, config_file: str)
    def run_pipeline_job(self, environment: str) -> Dict
    def run_manual_job(self, environment: str) -> Dict
    def get_pipeline_status(self) -> Dict
    def get_job_history(self, limit: int) -> List[Dict]
```

### DataValidator Class
```python
class DataValidator:
    @staticmethod
    def validate_patient_data(df: pd.DataFrame) -> Tuple[bool, List[str]]
    @staticmethod
    def validate_admission_data(df: pd.DataFrame) -> Tuple[bool, List[str]]
    @staticmethod
    def validate_financial_data(df: pd.DataFrame) -> Tuple[bool, List[str]]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Check the configuration file
4. Open an issue on GitHub

## 🔮 Future Enhancements

- **Real-time Streaming**: Support for real-time data streaming
- **Machine Learning**: Automated anomaly detection and data quality scoring
- **Advanced Analytics**: Built-in analytics and reporting features
- **Cloud Integration**: AWS, Azure, and GCP integration
- **Data Lineage**: End-to-end data lineage tracking
- **Advanced Scheduling**: DAG-based workflow scheduling
- **Multi-tenant Support**: Support for multiple organizations
- **API Gateway**: RESTful API for pipeline management
