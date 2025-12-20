import csv
import random

# Read existing department data
existing_dept_data = []
with open('data/department_metrics.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing_dept_data.append(row)

print(f"Current department rows: {len(existing_dept_data)}")

# Additional departments to reach ~17 departments (200/12 = 16.67)
additional_departments = [
    ('DEPT012', 'Gastroenterology'),
    ('DEPT013', 'Dermatology'),
    ('DEPT014', 'Urology'),
    ('DEPT015', 'Nephrology'),
    ('DEPT016', 'Pulmonology')
]

# Generate department metrics for 2022, 2023, 2024
all_dept_data = []
years = [2022, 2023, 2024]

# Get all 17 departments
all_departments = []
for row in existing_dept_data[:12]:  # First 12 from existing
    all_departments.append((row['department_id'], row['department_name']))
all_departments.extend(additional_departments)

for year in years:
    for dept_id, dept_name in all_departments:
        for month in range(1, 13):
            # Generate realistic metrics with year-over-year growth
            year_factor = 1 + (year - 2022) * 0.05  # 5% growth per year
            
            total_admissions = int(random.randint(50, 200) * year_factor)
            avg_length_of_stay = round(random.uniform(2.0, 10.0), 1)
            avg_cost = int(random.randint(3000, 15000) * year_factor)
            total_revenue = int(total_admissions * avg_cost * random.uniform(0.9, 1.1))
            occupancy_rate = round(random.uniform(0.60, 0.95), 2)
            nurse_patient_ratio = round(random.uniform(1.0, 3.0), 1)
            
            all_dept_data.append({
                'department_id': dept_id,
                'department_name': dept_name,
                'month': month,
                'year': year,
                'total_admissions': total_admissions,
                'avg_length_of_stay': avg_length_of_stay,
                'avg_cost': avg_cost,
                'total_revenue': total_revenue,
                'occupancy_rate': occupancy_rate,
                'nurse_patient_ratio': nurse_patient_ratio
            })

# Write department metrics
with open('data/department_metrics.csv', 'w', newline='') as f:
    fieldnames = ['department_id', 'department_name', 'month', 'year', 'total_admissions',
                  'avg_length_of_stay', 'avg_cost', 'total_revenue', 'occupancy_rate', 
                  'nurse_patient_ratio']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_dept_data)

print(f"New department rows: {len(all_dept_data)} ({len(all_departments)} departments × 12 months × 3 years)")

# Generate financial performance data that aggregates from department data
financial_data = []
for year in years:
    for month in range(1, 13):
        # Sum up department revenues for this month
        monthly_dept_data = [d for d in all_dept_data if d['year'] == year and d['month'] == month]
        total_revenue = sum(int(d['total_revenue']) for d in monthly_dept_data)
        
        # Generate expenses as 70-95% of revenue
        expense_ratio = random.uniform(0.70, 0.95)
        total_expenses = int(total_revenue * expense_ratio)
        net_income = total_revenue - total_expenses
        
        # Calculate operating margin
        operating_margin = round(net_income / total_revenue if total_revenue > 0 else 0, 3)
        
        # Generate other financial metrics as % of revenue
        bad_debt = int(total_revenue * random.uniform(0.02, 0.05))
        charity_care = int(total_revenue * random.uniform(0.01, 0.03))
        insurance_contractual = int(total_revenue * random.uniform(0.03, 0.08))
        cash_on_hand = int(total_revenue * random.uniform(0.15, 0.40))
        
        financial_data.append({
            'month': month,
            'year': year,
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_income': net_income,
            'operating_margin': operating_margin,
            'bad_debt': bad_debt,
            'charity_care': charity_care,
            'insurance_contractual': insurance_contractual,
            'cash_on_hand': cash_on_hand
        })

# Write financial performance
with open('data/financial_performance.csv', 'w', newline='') as f:
    fieldnames = ['month', 'year', 'total_revenue', 'total_expenses', 'net_income',
                  'operating_margin', 'bad_debt', 'charity_care', 'insurance_contractual',
                  'cash_on_hand']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(financial_data)

print(f"Financial performance rows: {len(financial_data)} (12 months × 3 years)")
print("\nSummary:")
print(f"- Years: 2022, 2023, 2024")
print(f"- Departments: {len(all_departments)} departments")
print(f"- Department metrics: {len(all_dept_data)} rows (~204 per year)")
print(f"- Financial data: {len(financial_data)} rows (12 per year)")
