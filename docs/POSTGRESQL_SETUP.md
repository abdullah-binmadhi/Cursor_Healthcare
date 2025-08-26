# PostgreSQL Healthcare Analytics Setup Guide

This guide provides step-by-step instructions for setting up and using the PostgreSQL version of the healthcare analytics system.

## Prerequisites

### 1. PostgreSQL Installation
- **macOS**: `brew install postgresql`
- **Ubuntu/Debian**: `sudo apt-get install postgresql postgresql-contrib`
- **Windows**: Download from [PostgreSQL official website](https://www.postgresql.org/download/windows/)

### 2. Python Dependencies
```bash
pip install -r requirements.txt
```

## Database Setup

### 1. Create PostgreSQL Database
```bash
# Connect to PostgreSQL as superuser
sudo -u postgres psql

# Create database and user
CREATE DATABASE healthcare_analytics;
CREATE USER healthcare_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE healthcare_analytics TO healthcare_user;
\q
```

### 2. Environment Variables
Set up your database connection parameters:

```bash
# Option 1: Export environment variables
export DB_USER=healthcare_user
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=healthcare_analytics

# Option 2: Create .env file
echo "DB_USER=healthcare_user" > .env
echo "DB_PASSWORD=your_password" >> .env
echo "DB_HOST=localhost" >> .env
echo "DB_PORT=5432" >> .env
echo "DB_NAME=healthcare_analytics" >> .env
```

## Quick Start

### 1. Set Up PostgreSQL Database
```bash
python postgresql_healthcare_setup.py
```

This script will:
- Create the database schema with 8 tables
- Load the healthcare dataset (10,000 records)
- Create performance indexes
- Test the connection

### 2. Run Analytics Queries
```bash
# Test connection
python postgresql_analytics_queries.py --test

# Run all analytics queries
python postgresql_analytics_queries.py

# Run specific query (e.g., query #3)
python postgresql_analytics_queries.py 3
```

## Database Schema

### Tables Created
1. **patients** - Patient demographics and insurance information
2. **admissions** - Hospital admission records with computed length of stay
3. **diagnoses** - Medical conditions and ICD codes
4. **procedures** - Treatments and procedures performed
5. **financial_data** - Billing and payment information with computed net revenue
6. **readmissions** - Track return visits
7. **quality_metrics** - Patient outcomes and satisfaction scores
8. **vital_signs** - Clinical measurements with computed BMI

### PostgreSQL-Specific Features
- **Generated Columns**: Length of stay and net revenue are automatically calculated
- **Foreign Key Constraints**: Proper referential integrity
- **Check Constraints**: Data validation (e.g., gender values, admission types)
- **Performance Indexes**: Optimized for analytics queries

## Analytics Queries

### Available Queries (15 total)
1. **Current Patient Census by Department**
2. **Monthly Admission Trends (12 months)**
3. **Top Diagnoses by Volume**
4. **Readmission Analysis (30 days)**
5. **Patient Satisfaction by Department**
6. **Daily Admission Volume Trend**
7. **Length of Stay Distribution**
8. **Revenue Analysis by Insurance Type**
9. **High-Volume Physicians**
10. **Weekend vs Weekday Admissions**
11. **Emergency vs Elective Admissions**
12. **Patient Age Distribution by Diagnosis**
13. **Room Utilization Analysis**
14. **Procedure Cost Analysis**
15. **Financial Performance Summary**

### PostgreSQL Syntax Features
- **TO_CHAR()** for date formatting
- **EXTRACT()** for date/time components
- **INTERVAL** for date arithmetic
- **GENERATED ALWAYS AS** for computed columns
- **::DECIMAL** for type casting

## Usage Examples

### 1. Direct Database Connection
```python
import pandas as pd
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine('postgresql://user:password@localhost:5432/healthcare_analytics')

# Run analytics query
df = pd.read_sql_query("""
    SELECT 
        d.diagnosis_description,
        COUNT(*) as case_count,
        ROUND(AVG(a.length_of_stay), 1) as avg_los
    FROM diagnoses d
    JOIN admissions a ON d.admission_id = a.admission_id
    WHERE d.diagnosis_type = 'Primary'
    GROUP BY d.diagnosis_description
    ORDER BY case_count DESC
    LIMIT 10
""", engine)

print(df)
```

### 2. Using psql Command Line
```bash
# Connect to database
psql -h localhost -U healthcare_user -d healthcare_analytics

# Run analytics query
SELECT 
    d.diagnosis_description,
    COUNT(*) as case_count,
    ROUND(AVG(a.length_of_stay), 1) as avg_los
FROM diagnoses d
JOIN admissions a ON d.admission_id = a.admission_id
WHERE d.diagnosis_type = 'Primary'
GROUP BY d.diagnosis_description
ORDER BY case_count DESC
LIMIT 10;
```

### 3. Performance Monitoring
```sql
-- Check table sizes
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE tablename IN ('patients', 'admissions', 'diagnoses', 'financial_data')
ORDER BY tablename, attname;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

## Performance Optimization

### 1. Additional Indexes
```sql
-- Create additional indexes for better performance
CREATE INDEX CONCURRENTLY idx_admissions_physician ON admissions(attending_physician);
CREATE INDEX CONCURRENTLY idx_admissions_type_date ON admissions(admission_type, admission_date);
CREATE INDEX CONCURRENTLY idx_financial_revenue ON financial_data(net_revenue);
CREATE INDEX CONCURRENTLY idx_diagnoses_description ON diagnoses(diagnosis_description);
```

### 2. Partitioning (for large datasets)
```sql
-- Partition admissions table by date (PostgreSQL 10+)
CREATE TABLE admissions_partitioned (
    LIKE admissions INCLUDING ALL
) PARTITION BY RANGE (admission_date);

-- Create monthly partitions
CREATE TABLE admissions_2024_01 PARTITION OF admissions_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### 3. Vacuum and Analyze
```sql
-- Regular maintenance
VACUUM ANALYZE patients;
VACUUM ANALYZE admissions;
VACUUM ANALYZE diagnoses;
VACUUM ANALYZE financial_data;
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   ```bash
   # Check if PostgreSQL is running
   sudo systemctl status postgresql
   
   # Start PostgreSQL
   sudo systemctl start postgresql
   ```

2. **Authentication Failed**
   ```bash
   # Check pg_hba.conf configuration
   sudo nano /etc/postgresql/*/main/pg_hba.conf
   
   # Restart PostgreSQL
   sudo systemctl restart postgresql
   ```

3. **Permission Denied**
   ```sql
   -- Grant necessary permissions
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO healthcare_user;
   GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO healthcare_user;
   ```

4. **Memory Issues**
   ```sql
   -- Adjust PostgreSQL configuration
   ALTER SYSTEM SET shared_buffers = '256MB';
   ALTER SYSTEM SET work_mem = '4MB';
   ALTER SYSTEM SET maintenance_work_mem = '64MB';
   SELECT pg_reload_conf();
   ```

## Backup and Recovery

### 1. Create Backup
```bash
# Full database backup
pg_dump -h localhost -U healthcare_user -d healthcare_analytics > backup.sql

# Compressed backup
pg_dump -h localhost -U healthcare_user -d healthcare_analytics | gzip > backup.sql.gz
```

### 2. Restore Database
```bash
# Restore from backup
psql -h localhost -U healthcare_user -d healthcare_analytics < backup.sql

# Restore from compressed backup
gunzip -c backup.sql.gz | psql -h localhost -U healthcare_user -d healthcare_analytics
```

## Monitoring and Maintenance

### 1. Regular Maintenance Script
```bash
#!/bin/bash
# maintenance.sh

# Vacuum and analyze all tables
psql -h localhost -U healthcare_user -d healthcare_analytics -c "
VACUUM ANALYZE patients;
VACUUM ANALYZE admissions;
VACUUM ANALYZE diagnoses;
VACUUM ANALYZE financial_data;
VACUUM ANALYZE procedures;
"

# Check database size
psql -h localhost -U healthcare_user -d healthcare_analytics -c "
SELECT 
    pg_size_pretty(pg_database_size('healthcare_analytics')) as database_size;
"
```

### 2. Performance Monitoring
```sql
-- Monitor slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

## Next Steps

1. **Set up automated data loading** from your healthcare systems
2. **Create additional indexes** based on your query patterns
3. **Implement data partitioning** for large datasets
4. **Set up regular backups** and monitoring
5. **Create custom analytics dashboards** using tools like Grafana or Tableau
6. **Implement data archiving** for historical data management

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review PostgreSQL documentation
3. Check the SQLite version for comparison
4. Examine the analytics query results for data validation
