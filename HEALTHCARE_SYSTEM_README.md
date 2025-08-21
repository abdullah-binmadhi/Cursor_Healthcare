# Healthcare Analytics System

A comprehensive healthcare analytics platform with data pipeline, web dashboard, and API endpoints for healthcare data management and analysis.

## 🏥 System Overview

This healthcare analytics system provides:

- **Data Pipeline**: ETL process for healthcare data processing
- **Web Dashboard**: Interactive web interface for data visualization
- **API Endpoints**: RESTful APIs for data access
- **Database Management**: SQLite database with comprehensive schema
- **Data Enrichment**: Tools to populate missing data and create additional datasets
- **Analytics**: Comprehensive healthcare metrics and reporting

## 📁 Project Structure

```
Cursor_Healthcare/
├── healthcare_web_app.py          # Main web application
├── healthcare_pipeline.py         # ETL pipeline
├── pipeline_scheduler.py          # Pipeline scheduling and monitoring
├── data_enrichment.py             # Data enrichment and generation
├── healthcare_analytics.db        # SQLite database
├── healthcare_dataset.csv         # Original dataset
├── healthcare_dataset_enriched.csv # Enriched dataset
├── requirements.txt               # Python dependencies
├── pipeline_config.yaml          # Pipeline configuration
├── api_endpoints.json            # API documentation
├── templates/                    # Web templates
│   ├── base.html
│   ├── dashboard.html
│   ├── analytics.html
│   ├── patients.html
│   ├── admissions.html
│   └── pipeline.html
├── Additional Datasets:
│   ├── physician_performance.csv
│   ├── department_metrics.csv
│   ├── quality_metrics.csv
│   ├── financial_performance.csv
│   └── patient_demographics.csv
└── Documentation:
    ├── README.md
    ├── PIPELINE_README.md
    └── POSTGRESQL_SETUP.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Enrich Data (Optional)

```bash
python data_enrichment.py
```

This will:
- Enhance the original dataset with missing fields
- Create additional datasets (physician performance, department metrics, etc.)
- Update the database schema
- Generate API documentation

### 3. Start the Web Application

```bash
python healthcare_web_app.py --host localhost --port 5000
```

### 4. Access the Dashboard

Open your browser and navigate to: `http://localhost:5000`

## 🌐 Web Dashboard Features

### Dashboard
- **Key Metrics**: Patient count, admission count, revenue, average charges
- **Recent Admissions**: Latest patient admissions with details
- **Top Diagnoses**: Most common medical conditions
- **Physician Performance**: Top performing physicians with metrics

### Analytics
- **Department Performance**: Metrics by hospital department
- **Quality Metrics**: Patient safety and quality indicators
- **Financial Performance**: Revenue, expenses, and profitability

### Data Management
- **Patients**: Browse and search patient records
- **Admissions**: View admission details and history
- **Pipeline**: Run data processing pipeline

## 🔌 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/metrics` | GET | Key performance metrics |
| `/api/patients` | GET | Patient information |
| `/api/admissions` | GET | Admission data |
| `/api/physicians` | GET | Physician performance |
| `/api/departments` | GET | Department metrics |
| `/api/quality` | GET | Quality indicators |
| `/api/financial` | GET | Financial performance |
| `/api/analytics` | GET | Comprehensive analytics data |

### Example API Usage

```bash
# Get key metrics
curl http://localhost:5000/api/metrics

# Get patient data (limit 50)
curl http://localhost:5000/api/patients?limit=50

# Get physician performance
curl http://localhost:5000/api/physicians?limit=10
```

## 📊 Database Schema

### Core Tables

#### Patients
- `patient_id` (Primary Key)
- `first_name`, `last_name`
- `date_of_birth`, `gender`
- `race`, `ethnicity`, `zip_code`
- `insurance_type`
- `created_date`, `updated_date`

#### Admissions
- `admission_id` (Primary Key)
- `patient_id` (Foreign Key)
- `admission_date`, `discharge_date`
- `admission_type`, `department`
- `attending_physician`
- `length_of_stay`
- `discharge_status`

#### Financial Data
- `financial_id` (Primary Key)
- `admission_id` (Foreign Key)
- `total_charges`, `insurance_payment`
- `patient_payment`, `net_revenue`
- `billing_date`

#### Diagnoses
- `diagnosis_id` (Primary Key)
- `admission_id` (Foreign Key)
- `diagnosis_code`, `diagnosis_description`
- `diagnosis_type`, `severity`

### Additional Tables

#### Physician Performance
- Monthly physician metrics
- Patient count, satisfaction scores
- Complication and readmission rates

#### Department Metrics
- Department-level performance
- Admissions, costs, revenue
- Occupancy rates

#### Quality Metrics
- Patient safety indicators
- Hospital-acquired infections
- Patient satisfaction scores

#### Financial Performance
- Monthly financial data
- Revenue, expenses, net income
- Operating margins

## 🔄 Data Pipeline

### Pipeline Components

1. **Data Extraction**: Read from CSV files
2. **Data Validation**: Quality checks and validation rules
3. **Data Transformation**: Cleaning and standardization
4. **Data Loading**: Insert into database tables
5. **Monitoring**: Track pipeline execution and performance

### Run Pipeline

```bash
# Via web interface
# Navigate to Pipeline page and click "Run Pipeline"

# Via Python
from healthcare_pipeline import HealthcarePipeline, PipelineConfig

config = PipelineConfig(
    source_type='csv',
    source_path='healthcare_dataset.csv',
    target_database='sqlite',
    target_connection='healthcare_analytics.db'
)

pipeline = HealthcarePipeline(config)
success = pipeline.run_pipeline()
```

## 📈 Data Enrichment

The data enrichment process adds:

### Enhanced Patient Data
- Demographics (race, ethnicity, zip code)
- Vital signs (blood pressure, heart rate, temperature)
- Lab results (glucose, creatinine, hemoglobin)
- Room types and severity scores
- Patient satisfaction scores

### Financial Breakdown
- Cost breakdown (room, medication, lab, procedure)
- Insurance coverage percentages
- Patient responsibility calculations

### Additional Datasets
- **Physician Performance**: Monthly metrics for each physician
- **Department Metrics**: Department-level performance data
- **Quality Metrics**: Patient safety and quality indicators
- **Financial Performance**: Monthly financial reports
- **Patient Demographics**: Demographic analysis by age, gender, insurance

## 🛠️ Configuration

### Pipeline Configuration (`pipeline_config.yaml`)

```yaml
source:
  type: csv
  path: healthcare_dataset.csv

target:
  database: sqlite
  connection: healthcare_analytics.db

processing:
  validation:
    max_errors: 1000
    allow_duplicates: true
  transformation:
    clean_names: true
    standardize_gender: true
    estimate_dob: true

monitoring:
  log_level: INFO
  metrics_collection: true
  alerting: true
```

## 🔧 Development

### Adding New Features

1. **New API Endpoints**: Add routes to `healthcare_web_app.py`
2. **Database Tables**: Update schema in data enrichment script
3. **Web Pages**: Create new templates in `templates/` directory
4. **Analytics**: Add new data manager methods

### Testing

```bash
# Test pipeline components
python test_pipeline_components.py

# Test data validation
python test_pipeline_validation.py

# Test web application
python healthcare_web_app.py --debug
```

## 📋 Data Sources

### Primary Dataset
- **File**: `healthcare_dataset.csv`
- **Records**: 10,000 patient admissions
- **Fields**: 15 original columns

### Enriched Dataset
- **File**: `healthcare_dataset_enriched.csv`
- **Records**: 10,000 patient admissions
- **Fields**: 40+ enhanced columns

### Additional Datasets
- **Physician Performance**: 180 records (15 physicians × 12 months)
- **Department Metrics**: 144 records (12 departments × 12 months)
- **Quality Metrics**: 12 records (monthly for 1 year)
- **Financial Performance**: 12 records (monthly for 1 year)
- **Patient Demographics**: 192 records (demographic breakdowns)

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Remove existing database and recreate
   rm healthcare_analytics.db
   python create_healthcare_database.py
   ```

2. **Missing Dependencies**
   ```bash
   pip install pandas sqlalchemy flask pyyaml schedule psutil
   ```

3. **Port Already in Use**
   ```bash
   # Use different port
   python healthcare_web_app.py --port 8080
   ```

4. **Pipeline Errors**
   ```bash
   # Check logs and validation
   python test_pipeline_validation.py
   ```

## 📚 API Documentation

### Response Formats

All API endpoints return JSON responses:

```json
{
  "data": [...],
  "count": 100,
  "status": "success"
}
```

### Error Responses

```json
{
  "error": "Error message",
  "status": "error"
}
```

### Pagination

Use `limit` parameter for pagination:
```
GET /api/patients?limit=50
```

## 🔒 Security Considerations

- **Local Deployment**: System designed for local deployment
- **No Authentication**: Basic setup without authentication
- **Data Privacy**: Ensure compliance with healthcare data regulations
- **Backup**: Regular database backups recommended

## 🚀 Future Enhancements

### Planned Features
- **User Authentication**: Role-based access control
- **Advanced Analytics**: Machine learning models
- **Real-time Monitoring**: Live data feeds
- **Mobile App**: React Native mobile application
- **Cloud Deployment**: AWS/Azure deployment options
- **Integration**: HL7 FHIR integration
- **Reporting**: Automated report generation
- **Alerts**: Real-time alerting system

### Technical Improvements
- **Performance**: Database optimization
- **Scalability**: Microservices architecture
- **Security**: Enhanced security measures
- **Testing**: Comprehensive test suite
- **Documentation**: API documentation with Swagger

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Test individual components
4. Verify database connectivity

## 📄 License

This project is for educational and demonstration purposes. Ensure compliance with healthcare data regulations when using with real patient data.
