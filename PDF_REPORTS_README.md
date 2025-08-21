# Healthcare Analytics PDF Reports

## 📊 Overview

This system generates downloadable PDF reports from your healthcare CSV data, providing comprehensive analytics dashboards without the need for a web server.

## 🚀 Quick Start

### Generate a Single Report
```bash
python pdf_dashboard_generator.py
```

### Generate Multiple Reports
```bash
python generate_all_reports.py
```

## 📄 Generated Reports

### Main Analytics Report (`healthcare_analytics_report.pdf`)
- **Summary Statistics**: Key metrics and KPIs
- **Patient Demographics**: Gender and age distributions
- **Financial Analytics**: Billing amounts and revenue analysis
- **Medical Conditions**: Top conditions and trends
- **Physician Performance**: Satisfaction scores and rankings
- **Department Metrics**: Length of stay and performance by department
- **Recent Patient Data**: Sample of recent admissions

### Executive Summary Report
- Condensed version for executive review
- Key performance indicators
- High-level trends and insights

## 📈 Charts Included

1. **Patient Gender Distribution** (Pie Chart)
2. **Patient Age Distribution** (Histogram)
3. **Billing Amount Distribution** (Histogram)
4. **Top Medical Conditions** (Bar Chart)
5. **Physician Satisfaction Rankings** (Horizontal Bar Chart)
6. **Department Length of Stay** (Bar Chart)

## 📊 Data Sources

The reports automatically load data from:
- `healthcare_dataset.csv` - Main patient data
- `healthcare_dataset_enriched.csv` - Enhanced patient data
- `physician_performance.csv` - Physician metrics
- `department_metrics.csv` - Department performance
- `quality_metrics.csv` - Quality indicators
- `financial_performance.csv` - Financial data
- `patient_demographics.csv` - Demographic information

## 🎨 Report Features

- **Professional Layout**: Clean, business-ready design
- **Color-Coded Sections**: Easy navigation and readability
- **High-Quality Charts**: 300 DPI resolution for crisp printing
- **Comprehensive Tables**: Detailed data presentation
- **Automatic Timestamps**: Reports include generation date/time

## 📁 File Locations

- **Single Report**: `healthcare_analytics_report.pdf` (in project root)
- **Multiple Reports**: `healthcare_reports/` directory
- **Chart Images**: Automatically cleaned up after PDF generation

## 🔧 Customization

You can modify the reports by editing `pdf_dashboard_generator.py`:
- Add new chart types
- Change color schemes
- Modify table layouts
- Add custom sections

## 📋 Requirements

- Python 3.7+
- pandas
- matplotlib
- seaborn
- reportlab

## 🎯 Benefits

✅ **No Web Server Required** - Generate reports locally
✅ **Professional Quality** - Print-ready PDF format
✅ **Comprehensive Analytics** - Multiple data sources
✅ **Easy Distribution** - Share via email or file sharing
✅ **Offline Access** - View reports without internet
✅ **Customizable** - Modify charts and layouts as needed

## 📞 Support

If you encounter any issues:
1. Ensure all CSV files are in the project directory
2. Check that all required Python packages are installed
3. Verify that CSV files have the expected column names

---

**Generated on**: {{ datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}
