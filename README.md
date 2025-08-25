# Healthcare Analytics - Database & Website Platform

A comprehensive healthcare analytics platform featuring both backend database systems and a modern web application for healthcare cost estimation and physician discovery.

## 🌐 Live Healthcare Website

**🔗 [Visit the Healthcare Website](https://abdullah-binmadhi.github.io/Cursor_Healthcare/healthcare-website/)**

Experience our interactive healthcare platform featuring:
- **💰 Healthcare Cost Estimator** - Get transparent pricing for medical procedures
- **👨‍⚕️ Doctor Finder & Ratings** - Search qualified physicians with performance metrics
- **📱 Mobile-Responsive Design** - Works seamlessly on all devices
- **📊 Real-Time Data** - Interactive filtering and cost calculations

### Website Features
- **Cost Estimation**: Input age, insurance type, department, and procedure for instant cost breakdowns
- **Physician Directory**: Search 150+ doctors across 7 specialties and 8 hospitals with ratings and availability
- **Transparent Pricing**: Clear breakdown of total costs, insurance coverage, and patient costs
- **Performance Metrics**: Doctor success rates, patient satisfaction scores, and wait times
- **Hospital Network**: Filter physicians by hospital affiliation across 8 medical centers

## Overview

This project combines powerful healthcare analytics databases with user-friendly web applications. The platform includes:

### 🖥️ **Web Application**
- Modern healthcare website with cost estimator and doctor finder
- Interactive forms and real-time data filtering
- Professional healthcare-themed design
- Mobile-first responsive interface

### 🗄️ **Database Systems**
- Comprehensive SQLite database for healthcare analytics
- PostgreSQL enterprise version for production environments
- Sample data with 10,000+ healthcare records
- Advanced analytics queries and database views

The databases are designed for analytics and reporting on patient admissions, diagnoses, procedures, and financial data, while the website provides public-facing tools for healthcare transparency.

## Files

### 🌐 Healthcare Website
- **`healthcare-website/`** - Complete web application directory
  - `index.html` - Main website with cost estimator and doctor finder
  - `style.css` - Modern healthcare-themed styling
  - `script.js` - Interactive functionality and data processing
  - `data/` - CSV files with healthcare data (physicians, costs, metrics)
  - `README.md` - Website documentation and setup guide
- **`generate_website_data.py`** - Script to generate sample healthcare data for website

### 🗄️ Database Systems

### SQLite Version (Default)
- `create_healthcare_database.py` - Main script to create and populate SQLite database
- `healthcare_schema_sqlite.sql` - SQLite-compatible database schema
- `test_database.py` - Test script to verify SQLite database functionality
- `run_analytics_queries.py` - Script to execute analytics queries on SQLite
- `healthcare_analytics_summary.py` - Comprehensive system summary and demonstration
- `Views for common queries.sql` - Predefined views for common analytics queries
- `create_views.py` - Script to create database views

### PostgreSQL Version (Enterprise)
- `postgresql_healthcare_setup.py` - Main script to create and populate PostgreSQL database
- `postgresql_analytics_queries.py` - Script to execute analytics queries on PostgreSQL
- `POSTGRESQL_SETUP.md` - Comprehensive PostgreSQL setup and usage guide

### Shared Files
- `healthcare_dataset.csv` - Sample healthcare data (10,000 records)
- `requirements.txt` - Python dependencies for both SQLite and PostgreSQL
- `Data Schema.sql` - Original PostgreSQL schema (for reference)
- `essential_analytics_queries.sql` - Collection of essential healthcare analytics queries
- `performance indexes.sql` - Database performance optimization indexes

## Database Schema

The database contains 8 main tables:

1. **patients** - Patient demographic and insurance information
2. **admissions** - Hospital admission records with length of stay
3. **diagnoses** - Medical conditions and ICD codes
4. **procedures** - Treatments and procedures performed
5. **financial_data** - Billing and payment information
6. **readmissions** - Track return visits (empty in sample data)
7. **quality_metrics** - Patient outcomes and satisfaction scores (empty in sample data)
8. **vital_signs** - Clinical measurements (empty in sample data)

## 🚀 Quick Start

### Use the Live Website (Recommended)
1. **Visit the website**: [https://abdullah-binmadhi.github.io/Cursor_Healthcare/healthcare-website/](https://abdullah-binmadhi.github.io/Cursor_Healthcare/healthcare-website/)
2. **Try the Cost Estimator**: Input patient information to get cost estimates
3. **Search for Doctors**: Filter physicians by specialty, ratings, and availability
4. **Explore Features**: Interactive forms, real-time calculations, and responsive design

### Run Website Locally
1. **Clone the repository**:
   ```bash
   git clone https://github.com/abdullah-binmadhi/Cursor_Healthcare.git
   cd Cursor_Healthcare/healthcare-website
   ```
2. **Start a local server**:
   ```bash
   python -m http.server 8080
   ```
3. **Open browser**: Visit `http://localhost:8080`

### Database Analytics

### SQLite Version (Quick Start)
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create the database:**
   ```bash
   python create_healthcare_database.py
   ```

3. **Test the database:**
   ```bash
   python test_database.py
   ```

4. **Create database views:**
   ```bash
   python create_views.py
   ```

5. **Run analytics queries:**
   ```bash
   python run_analytics_queries.py
   ```

6. **Generate comprehensive summary:**
   ```bash
   python healthcare_analytics_summary.py
   ```

### PostgreSQL Version (Enterprise)
1. **Install PostgreSQL** (see POSTGRESQL_SETUP.md for detailed instructions)
2. **Set up environment variables** for database connection
3. **Create and populate database:**
   ```bash
   python postgresql_healthcare_setup.py
   ```
4. **Run analytics queries:**
   ```bash
   python postgresql_analytics_queries.py
   ```
5. **For detailed setup instructions, see:** `POSTGRESQL_SETUP.md`

## Sample Data

The database is populated with 10,000 sample healthcare records including:
- 9,378 unique patients
- Various medical conditions (Asthma, Cancer, Hypertension, Arthritis, Obesity, Diabetes)
- Different admission types (Emergency, Elective, Urgent)
- Financial data with billing amounts and insurance payments
- Procedures and medications

## Analytics Queries and Views

### Essential Analytics Queries (15 queries)
The `essential_analytics_queries.sql` file contains 15 comprehensive healthcare analytics queries:

1. **Current Patient Census by Department** - Active patients and average days admitted
2. **Monthly Admission Trends** - 12-month admission and length of stay trends
3. **Top Diagnoses by Volume** - Most common conditions with revenue analysis
4. **Readmission Analysis** - 30-day readmission rates by department
5. **Patient Satisfaction by Department** - Quality metrics and satisfaction scores
6. **Daily Admission Volume Trend** - 30-day daily admission patterns
7. **Length of Stay Distribution** - LOS statistics by department
8. **Revenue Analysis by Insurance Type** - Financial performance by payer
9. **High-Volume Physicians** - Physician workload and performance
10. **Weekend vs Weekday Admissions** - Admission patterns analysis
11. **Emergency vs Elective Admissions** - Monthly comparison by type
12. **Patient Age Distribution by Diagnosis** - Age demographics by condition
13. **Room Utilization Analysis** - Room usage and revenue by room
14. **Procedure Cost Analysis** - Procedure costs and duration
15. **Financial Performance Summary** - Monthly financial metrics

### Database Views (8 views)
The `Views for common queries.sql` file creates 8 useful database views:

1. **patient_summary** - Patient demographics and admission history
2. **department_performance** - Department metrics and performance
3. **monthly_metrics** - Monthly admission and financial trends
4. **high_risk_patients** - Patients with high readmission risk
5. **current_census** - Current patient census by department
6. **top_diagnoses** - Most common diagnoses with metrics
7. **physician_performance** - Physician workload and performance
8. **financial_summary** - Monthly financial performance

## Database Statistics

- **Patients**: 9,378 records
- **Admissions**: 10,000 records
- **Diagnoses**: 10,000 records
- **Procedures**: 10,000 records
- **Financial Data**: 10,000 records

## Key Features

### SQLite Version
- **Lightweight Database**: Serverless, file-based database perfect for development and small-scale analytics
- **Quick Setup**: No server installation required
- **Portable**: Single file database that can be easily shared and backed up
- **Comprehensive Schema**: Covers all major healthcare data domains
- **Sample Data**: Realistic healthcare data for testing and development
- **Analytics Ready**: Optimized for healthcare analytics and reporting
- **Performance Indexes**: Pre-configured indexes for common queries

### PostgreSQL Version
- **Enterprise Database**: Robust, scalable database for production environments
- **Advanced Features**: Generated columns, foreign key constraints, check constraints
- **Performance**: Optimized for large datasets and complex queries
- **Concurrent Access**: Multiple users can access the database simultaneously
- **Backup & Recovery**: Built-in backup and recovery capabilities
- **Monitoring**: Advanced monitoring and performance tuning options
- **Scalability**: Can handle millions of records with proper indexing

## Usage Examples

### Basic Query
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('healthcare_analytics.db')

# Get patient count by gender
df = pd.read_sql_query("""
    SELECT gender, COUNT(*) as count 
    FROM patients 
    GROUP BY gender
""", conn)

print(df)
```

### Complex Analytics
```python
# Average length of stay by medical condition and admission type
df = pd.read_sql_query("""
    SELECT d.diagnosis_description,
           a.admission_type,
           AVG(a.length_of_stay) as avg_los,
           COUNT(*) as admission_count
    FROM admissions a
    JOIN diagnoses d ON a.admission_id = d.admission_id
    WHERE a.length_of_stay IS NOT NULL
    GROUP BY d.diagnosis_description, a.admission_type
    ORDER BY avg_los DESC
""", conn)

### Using Views
```python
# Get current patient census
df_census = pd.read_sql_query("SELECT * FROM current_census", conn)

# Get top diagnoses
df_diagnoses = pd.read_sql_query("SELECT * FROM top_diagnoses LIMIT 10", conn)

# Get physician performance
df_physicians = pd.read_sql_query("""
    SELECT * FROM physician_performance 
    WHERE total_cases > 10 
    ORDER BY avg_satisfaction DESC
""", conn)
```

### Running Analytics Queries
```bash
# Run all analytics queries
python run_analytics_queries.py

# List available queries
python run_analytics_queries.py --list

# Run specific query (e.g., query #3)
python run_analytics_queries.py 3
```

## Data Quality

The script includes data cleaning and validation:
- Handles missing values appropriately
- Converts data types (dates, numbers)
- Creates unique patient IDs
- Estimates missing fields (birth dates, financial breakdowns)
- Validates data constraints

## Performance Considerations

- Indexes are created on frequently queried columns
- Foreign key relationships are properly established
- Data types are optimized for SQLite
- Batch inserts are used for better performance

## Future Enhancements

- Add more sample data for readmissions, quality metrics, and vital signs
- Implement data visualization dashboards
- Add more complex analytics queries
- Create data export functionality
- Add data validation and quality checks

## License

This project is for educational and demonstration purposes.
