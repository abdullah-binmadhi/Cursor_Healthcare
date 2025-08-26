# 🏥 Cursor Healthcare Analytics Platform

> **Professional healthcare analytics and data visualization platform with comprehensive cost estimation, physician finder, and real-time analytics dashboard.**

## 🚀 Live Platform

### **[📊 Healthcare Analytics Dashboard](healthcare-website/index.html)** <sup>🆕</sup>

**Main Features:**
- 💰 **Smart Cost Estimator** - Real-time healthcare cost calculations
- 👩‍⚕️ **Advanced Doctor Finder** - Specialty-based physician search with filtering
- 📊 **Analytics Dashboard** - Interactive charts with hospital selection and multi-year data
- 🏥 **Hospital Selector** - Filter analytics by specific hospitals
- 📈 **Performance Trends** - Multi-year healthcare metrics visualization
- 🎯 **Quality Metrics** - Department and hospital quality scores

## 📁 Project Structure

```
Cursor_Healthcare/
├── 🌐 healthcare-website/          # Main Web Application
│   ├── index.html                  # Primary healthcare platform
│   ├── style.css                   # Main styling
│   ├── script.js                   # Core functionality
│   └── data/                       # Website data files
├── 📜 sql/                         # Database schemas and queries
│   ├── Data Schema.sql             # Main database schema
│   ├── essential_analytics_queries.sql
│   ├── healthcare_schema_sqlite.sql
│   └── Views for common queries.sql
├── 🔧 scripts/                     # Python utilities and tools
│   ├── create_healthcare_database.py
│   ├── healthcare_web_app.py       # Flask web server
│   ├── data_enrichment.py
│   └── postgresql_healthcare_setup.py
├── 📊 data/                        # Sample data and configurations
│   ├── department_metrics.csv
│   ├── pipeline_config.yaml
│   └── api_endpoints.json
├── 🧪 tests/                       # Test files
│   ├── test_database.py
│   └── test_pipeline_components.py
├── 📚 docs/                        # Documentation
│   ├── HEALTHCARE_SYSTEM_README.md
│   ├── POSTGRESQL_SETUP.md
│   └── PIPELINE_README.md
├── 📄 templates/                   # Flask templates (legacy)
└── 📋 requirements.txt             # Python dependencies
```

## ⚡ Quick Start

### Option 1: Direct Web Access (Recommended)
```bash
# Simply open the healthcare website
open healthcare-website/index.html
```

### Option 2: Python Flask Server
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python scripts/healthcare_web_app.py

# Visit: http://localhost:5000
```

## 🔧 Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js for interactive visualizations
- **Backend**: Python 3.x, Flask
- **Database**: SQLite (development), PostgreSQL (production)
- **Analytics**: Pandas, NumPy
- **Styling**: Modern CSS with backdrop filters and animations

## 📊 Features Showcase

### 🏥 Analytics Dashboard
- **Multi-Hospital Filtering**: Select specific hospitals for targeted analytics
- **Year-Based Comparison**: Compare data across 2022, 2023, and 2024
- **Interactive Charts**: Department performance, physician rankings, quality metrics
- **Real-Time Updates**: Dynamic chart synchronization across filters

### 💰 Cost Estimator
- **Procedure-Based Estimates**: Accurate cost calculations for medical procedures
- **Insurance Integration**: Support for different insurance types
- **Regional Variations**: Location-based cost adjustments

### 👩‍⚕️ Doctor Finder
- **Specialty Filtering**: Search by medical specialties
- **Location-Based Search**: Find nearby healthcare providers
- **Rating & Reviews**: Patient satisfaction scores

## 🛠️ Development

### Database Setup
```bash
# Create SQLite database
python scripts/create_healthcare_database.py

# For PostgreSQL (production)
python scripts/postgresql_healthcare_setup.py
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_database.py
```

## 📈 Analytics Capabilities

- **Healthcare Metrics**: Patient satisfaction, occupancy rates, quality scores
- **Financial Analysis**: Revenue tracking, cost analysis, performance metrics
- **Operational Insights**: Department efficiency, physician performance
- **Predictive Analytics**: Trend analysis and forecasting

## 🔒 Data Privacy

This platform uses **synthetic healthcare data** for demonstration purposes. All patient information is artificially generated and complies with privacy standards.

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ for modern healthcare analytics**