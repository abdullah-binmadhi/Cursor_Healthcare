import csv
import random
from collections import defaultdict

print("Generating cohesive healthcare system data...\n")

# Define the healthcare system structure
YEARS = [2022, 2023, 2024]
DEPARTMENTS = [
    ('DEPT000', 'Emergency Medicine', ['PHY000', 'PHY001', 'PHY002', 'PHY003', 'PHY004', 'PHY005']),
    ('DEPT001', 'Cardiology', ['PHY006', 'PHY007', 'PHY008', 'PHY009', 'PHY010', 'PHY011']),
    ('DEPT002', 'Orthopedics', ['PHY012', 'PHY013', 'PHY014', 'PHY015', 'PHY016', 'PHY017']),
    ('DEPT003', 'Neurology', ['PHY018', 'PHY019', 'PHY020', 'PHY021', 'PHY022', 'PHY023']),
    ('DEPT004', 'Oncology', ['PHY024', 'PHY025', 'PHY026', 'PHY027', 'PHY028', 'PHY029']),
    ('DEPT005', 'Pediatrics', ['PHY030', 'PHY031', 'PHY032', 'PHY033', 'PHY034', 'PHY035']),
    ('DEPT006', 'Internal Medicine', ['PHY036', 'PHY037', 'PHY038', 'PHY039', 'PHY040', 'PHY041']),
    ('DEPT007', 'Surgery', ['PHY042', 'PHY043', 'PHY044', 'PHY045', 'PHY046', 'PHY047']),
    ('DEPT008', 'Psychiatry', ['PHY048', 'PHY049', 'PHY050', 'PHY051', 'PHY052', 'PHY053']),
    ('DEPT009', 'Radiology', ['PHY054', 'PHY055', 'PHY056', 'PHY057', 'PHY058', 'PHY059']),
    ('DEPT010', 'Anesthesiology', ['PHY060', 'PHY061', 'PHY062', 'PHY063', 'PHY064', 'PHY065']),
    ('DEPT011', 'Obstetrics', ['PHY066', 'PHY067', 'PHY068', 'PHY069', 'PHY070', 'PHY071']),
    ('DEPT012', 'Gastroenterology', ['PHY072', 'PHY073', 'PHY074', 'PHY075', 'PHY076']),
    ('DEPT013', 'Dermatology', ['PHY077', 'PHY078', 'PHY079', 'PHY080', 'PHY081']),
    ('DEPT014', 'Urology', ['PHY082', 'PHY083', 'PHY084', 'PHY085', 'PHY086']),
    ('DEPT015', 'Nephrology', ['PHY087', 'PHY088', 'PHY089', 'PHY090', 'PHY091']),
    ('DEPT016', 'Pulmonology', ['PHY092', 'PHY093', 'PHY094', 'PHY095', 'PHY096', 'PHY097', 'PHY098', 'PHY099'])
]

# Physician names
FIRST_NAMES = ['Sarah', 'Michael', 'Emily', 'David', 'Lisa', 'Robert', 'Jennifer', 'Christopher',
               'Amanda', 'James', 'Michelle', 'Thomas', 'Rachel', 'Daniel', 'Jessica', 'John',
               'Mary', 'William', 'Patricia', 'Richard', 'Linda', 'Joseph', 'Barbara', 'Charles',
               'Elizabeth', 'Steven', 'Susan', 'Matthew', 'Karen', 'Anthony', 'Nancy', 'Mark',
               'Betty', 'Donald', 'Margaret', 'Paul', 'Sandra', 'Andrew', 'Ashley', 'Joshua']

LAST_NAMES = ['Johnson', 'Chen', 'Rodriguez', 'Kim', 'Thompson', 'Wilson', 'Davis', 'Brown',
              'Garcia', 'Miller', 'Lee', 'Anderson', 'White', 'Martinez', 'Taylor', 'Smith',
              'Williams', 'Jones', 'Moore', 'Jackson', 'Martin', 'Perez', 'Harris', 'Clark',
              'Lewis', 'Robinson', 'Walker', 'Young', 'Hall', 'Allen', 'King', 'Wright',
              'Scott', 'Torres', 'Nguyen', 'Hill', 'Green', 'Adams', 'Baker', 'Nelson']

# Generate physician registry
physician_registry = {}
name_index = 0
for dept_id, dept_name, physicians in DEPARTMENTS:
    for phy_id in physicians:
        if name_index < len(FIRST_NAMES):
            physician_registry[phy_id] = {
                'name': f"Dr. {FIRST_NAMES[name_index % len(FIRST_NAMES)]} {LAST_NAMES[name_index % len(LAST_NAMES)]}",
                'department': dept_name,
                'department_id': dept_id
            }
            name_index += 1

print(f"Created {len(physician_registry)} physicians across {len(DEPARTMENTS)} departments")

# STEP 1: Generate Department Metrics
department_data = []
dept_monthly_revenue = defaultdict(lambda: defaultdict(int))

for year in YEARS:
    year_factor = 1 + (year - 2022) * 0.05  # 5% growth
    for dept_id, dept_name, physicians in DEPARTMENTS:
        for month in range(1, 13):
            admissions = int(random.randint(60, 180) * year_factor)
            avg_los = round(random.uniform(2.5, 8.5), 1)
            avg_cost = int(random.randint(4000, 14000) * year_factor)
            revenue = int(admissions * avg_cost * random.uniform(0.95, 1.05))
            
            dept_monthly_revenue[year][month] += revenue
            
            department_data.append({
                'department_id': dept_id,
                'department_name': dept_name,
                'month': month,
                'year': year,
                'total_admissions': admissions,
                'avg_length_of_stay': avg_los,
                'avg_cost': avg_cost,
                'total_revenue': revenue,
                'occupancy_rate': round(random.uniform(0.65, 0.92), 2),
                'nurse_patient_ratio': round(random.uniform(1.2, 2.8), 1)
            })

print(f"Generated {len(department_data)} department records")

# STEP 2: Generate Physician Performance (aligned with departments)
physician_data = []
for phy_id, phy_info in physician_registry.items():
    for year in YEARS:
        for month in range(1, 13):
            # Physician performance contributes to department metrics
            patients = random.randint(12, 48)
            avg_los = round(random.uniform(2.0, 8.0), 1)
            satisfaction = round(random.uniform(3.6, 5.0), 1)
            complication_rate = round(random.uniform(0.05, 0.19), 3)
            readmission_rate = round(random.uniform(0.10, 0.24), 3)
            revenue = random.randint(6000, 24000)
            
            physician_data.append({
                'physician_id': phy_id,
                'physician_name': phy_info['name'],
                'month': month,
                'year': year,
                'total_patients': patients,
                'avg_length_of_stay': avg_los,
                'avg_satisfaction_score': satisfaction,
                'complication_rate': complication_rate,
                'readmission_rate': readmission_rate,
                'avg_revenue': revenue
            })

print(f"Generated {len(physician_data)} physician performance records")

# STEP 3: Generate Patient Demographics (aligned with admissions)
age_groups = ['0-17', '18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
genders = ['M', 'F']
insurance_types = ['Blue Cross Blue Shield', 'Aetna', 'Cigna', 'UnitedHealthcare', 'Humana',
                   'Kaiser Permanente', 'Anthem', 'Medicare', 'Medicaid', 'Tricare',
                   'Health Net', 'Molina Healthcare']

patient_data = []
# Generate ~1000 demographic segments
segments_needed = 1000
segment_count = 0

while segment_count < segments_needed:
    age = random.choice(age_groups)
    gender = random.choice(genders)
    insurance = random.choice(insurance_types)
    
    # Patient counts that sum up to realistic hospital volumes
    patient_count = random.randint(55, 285)
    avg_los = round(random.uniform(2.2, 7.8), 1)
    avg_cost = random.randint(3200, 11800)
    readmission = round(random.uniform(0.10, 0.25), 3)
    
    patient_data.append({
        'age_group': age,
        'gender': gender,
        'insurance_type': insurance,
        'patient_count': patient_count,
        'avg_length_of_stay': avg_los,
        'avg_cost': avg_cost,
        'readmission_rate': readmission
    })
    segment_count += 1

# Sort by age group
age_order = {age: i for i, age in enumerate(age_groups)}
patient_data.sort(key=lambda x: (age_order[x['age_group']], x['gender'], x['insurance_type']))

print(f"Generated {len(patient_data)} patient demographic segments")

# STEP 4: Generate Financial Performance (aggregated from departments)
financial_data = []
for year in YEARS:
    for month in range(1, 13):
        total_revenue = dept_monthly_revenue[year][month]
        expense_ratio = random.uniform(0.72, 0.93)
        total_expenses = int(total_revenue * expense_ratio)
        net_income = total_revenue - total_expenses
        operating_margin = round(net_income / total_revenue if total_revenue > 0 else 0, 3)
        
        financial_data.append({
            'month': month,
            'year': year,
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_income': net_income,
            'operating_margin': operating_margin,
            'bad_debt': int(total_revenue * random.uniform(0.025, 0.048)),
            'charity_care': int(total_revenue * random.uniform(0.012, 0.028)),
            'insurance_contractual': int(total_revenue * random.uniform(0.035, 0.075)),
            'cash_on_hand': int(total_revenue * random.uniform(0.18, 0.38))
        })

print(f"Generated {len(financial_data)} financial performance records")

# Write all files to both locations
for location in ['data', 'healthcare-website/data']:
    # Department Metrics
    with open(f'{location}/department_metrics.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['department_id', 'department_name', 'month', 'year',
                                                'total_admissions', 'avg_length_of_stay', 'avg_cost',
                                                'total_revenue', 'occupancy_rate', 'nurse_patient_ratio'])
        writer.writeheader()
        writer.writerows(department_data)
    
    # Physician Performance
    with open(f'{location}/physician_performance.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['physician_id', 'physician_name', 'month', 'year',
                                                'total_patients', 'avg_length_of_stay',
                                                'avg_satisfaction_score', 'complication_rate',
                                                'readmission_rate', 'avg_revenue'])
        writer.writeheader()
        writer.writerows(physician_data)
    
    # Patient Demographics
    with open(f'{location}/patient_demographics.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['age_group', 'gender', 'insurance_type',
                                                'patient_count', 'avg_length_of_stay',
                                                'avg_cost', 'readmission_rate'])
        writer.writeheader()
        writer.writerows(patient_data)
    
    # Financial Performance
    with open(f'{location}/financial_performance.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['month', 'year', 'total_revenue', 'total_expenses',
                                                'net_income', 'operating_margin', 'bad_debt',
                                                'charity_care', 'insurance_contractual', 'cash_on_hand'])
        writer.writeheader()
        writer.writerows(financial_data)

print(f"\n✓ All files written to both 'data/' and 'healthcare-website/data/'")
print("\n=== COHESIVE DATA SUMMARY ===")
print(f"Years: {min(YEARS)}-{max(YEARS)}")
print(f"Departments: {len(DEPARTMENTS)}")
print(f"Physicians: {len(physician_registry)} (assigned to departments)")
print(f"Department metrics: {len(department_data)} rows")
print(f"Physician performance: {len(physician_data)} rows")
print(f"Patient demographics: {len(patient_data)} segments")
print(f"Financial performance: {len(financial_data)} rows")
print("\nRelationships:")
print("- Each physician is assigned to a specific department")
print("- Financial totals = sum of all department revenues by month")
print("- Patient demographics represent hospital population")
print("- All data spans same time period (2022-2024)")
