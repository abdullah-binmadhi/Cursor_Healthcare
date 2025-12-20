# 🏥 Cursor Healthcare Analytics Platform

> **Professional healthcare analytics and data visualization platform with ML-powered readmission prediction, cost estimation, physician finder, and comprehensive analytics dashboards.**

[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge)](https://abdullah-binmadhi.github.io/Cursor_Healthcare/healthcare-website/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-black?style=for-the-badge&logo=vercel)](https://vercel.com)

## 🚀 Live Platform

### **[→ Launch Healthcare Analytics Dashboard](https://abdullah-binmadhi.github.io/Cursor_Healthcare/healthcare-website/)**

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📊 **Analytics Dashboard** | Interactive charts with hospital selection, multi-year data (2022-2024) |
| 🤖 **ML Readmission Prediction** | Random Forest & XGBoost models with SMOTE balancing |
| 💰 **Smart Cost Estimator** | Real-time healthcare cost calculations by procedure & insurance |
| 👨‍⚕️ **Doctor Finder** | Specialty-based physician search with ratings & filtering |
| 📈 **14 Data Visualizations** | Comprehensive graphs for model comparison, demographics, trends |
| 📄 **PDF Reports** | Auto-generated comprehensive analysis reports |

---

## 📁 Project Structure

```
Cursor_Healthcare/
├── healthcare-website-v2/     # React Web Application (Current)
│   ├── src/
│   │   ├── pages/             # Home, Analytics, DoctorFinder, CostEstimator
│   │   ├── components/        # UI components
│   │   └── services/          # Supabase integration
│   └── package.json
├── ML-models/                 # Machine Learning Pipeline
│   ├── healthcare_ml_pipeline.py      # RF & XGBoost training
│   ├── generate_all_visualizations.py # 14 graph generation
│   └── generate_comprehensive_reports.py # PDF reports
├── graphs/                    # Generated Outputs
│   ├── *.png                  # 14 visualization files
│   ├── Healthcare_Dataset_Report.pdf
│   └── Healthcare_ML_Models_Report.pdf
├── data/                      # Datasets
│   ├── patient_demographics.csv
│   ├── physician_performance.csv
│   ├── department_metrics.csv
│   ├── financial_performance.csv
│   └── physician_registry.csv
├── scripts/                   # Utilities
│   ├── data_generation/       # Data generation scripts
│   └── database/              # Supabase migration tools
├── sql/                       # Database Schemas
├── docs/                      # Documentation
│   └── changelogs/            # Update logs
└── tests/                     # Test files
```

---

## 🧠 Machine Learning Models

### Readmission Risk Prediction

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| **Random Forest** | 58.80% | 37.18% | 34.94% | 36.02% | 0.5353 |
| **XGBoost** | 55.60% | 34.78% | 38.55% | 36.57% | 0.5215 |

**Key Features:**

- SMOTE class balancing for imbalanced data
- 6 input features: age, gender, insurance, patient count, length of stay, cost
- Binary classification: High Risk (>20% readmission) vs Low Risk

---

## 📊 Visualizations

14 comprehensive graphs generated:

1. Model Comparison Metrics
2. Confusion Matrices
3. ROC Curves
4. Feature Importance
5. Precision-Recall Analysis
6. Accuracy & F1-Score
7. Model Summary Table
8. **Demographics Distribution**
9. **Readmission Rate Analysis**
10. **Physician Performance Trends**
11. **Department Comparison**
12. **Financial Dashboard**
13. **Correlation Heatmap**
14. **Cost Analysis**

---

## 🛠️ Quick Start

### Web Application

```bash
cd healthcare-website-v2
npm install
npm run dev
# Visit: http://localhost:5173
```

### Generate ML Visualizations

```bash
cd ML-models
python generate_all_visualizations.py
```

### Generate PDF Reports

```bash
cd ML-models
python generate_comprehensive_reports.py
```

---

## 🔧 Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React, Vite, Tailwind CSS, Recharts |
| **Backend** | Supabase (PostgreSQL) |
| **ML** | Python, scikit-learn, XGBoost, SMOTE |
| **Visualization** | Matplotlib, Seaborn |
| **Reports** | ReportLab (PDF generation) |
| **Deployment** | Vercel, GitHub Pages |

---

## 📦 Datasets

| Dataset | Records | Description |
|---------|---------|-------------|
| patient_demographics.csv | 1,001 | Patient characteristics & outcomes |
| physician_performance.csv | 3,960 | Monthly physician metrics |
| department_metrics.csv | 612 | Department operations |
| financial_performance.csv | 36 | Hospital financials (2022-2024) |
| physician_registry.csv | 110 | Physician directory |

---

## 🔒 Data Privacy

This platform uses **synthetic healthcare data** for demonstration purposes. All patient information is artificially generated and complies with privacy standards.

---

## 📜 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ for modern healthcare analytics**
