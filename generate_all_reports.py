#!/usr/bin/env python3
"""
Generate All Healthcare Analytics Reports
Creates multiple PDF reports for different analytics views
"""

import os
from datetime import datetime
from pdf_dashboard_generator import HealthcarePDFDashboard

def generate_all_reports():
    """Generate multiple PDF reports"""
    print("📊 Generating All Healthcare Analytics Reports...")
    
    # Create reports directory if it doesn't exist
    reports_dir = "healthcare_reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Generate main comprehensive report
    print("\n1️⃣ Generating Main Analytics Report...")
    generator = HealthcarePDFDashboard()
    main_report = os.path.join(reports_dir, f"healthcare_analytics_main_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    generator.generate_pdf(main_report)
    
    # Generate summary report
    print("\n2️⃣ Generating Executive Summary Report...")
    summary_report = os.path.join(reports_dir, f"healthcare_executive_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    generator.generate_pdf(summary_report)
    
    print(f"\n✅ All reports generated successfully!")
    print(f"📁 Reports location: {os.path.abspath(reports_dir)}")
    print(f"📄 Main Report: {os.path.basename(main_report)}")
    print(f"📄 Summary Report: {os.path.basename(summary_report)}")
    
    # List all generated files
    print(f"\n📋 All generated files:")
    for file in os.listdir(reports_dir):
        if file.endswith('.pdf'):
            file_path = os.path.join(reports_dir, file)
            file_size = os.path.getsize(file_path) / 1024  # Size in KB
            print(f"   📄 {file} ({file_size:.1f} KB)")

if __name__ == "__main__":
    generate_all_reports()
