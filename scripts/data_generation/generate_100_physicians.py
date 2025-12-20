import csv
import random

print("Generating 100 physicians with cohesive data...\n")

# Define the healthcare system with 100 physicians
DEPARTMENTS = [
    ('DEPT000', 'Emergency Medicine', 8),
    ('DEPT001', 'Cardiology', 8),
    ('DEPT002', 'Orthopedics', 7),
    ('DEPT003', 'Neurology', 7),
    ('DEPT004', 'Oncology', 7),
    ('DEPT005', 'Pediatrics', 7),
    ('DEPT006', 'Internal Medicine', 7),
    ('DEPT007', 'Surgery', 8),
    ('DEPT008', 'Psychiatry', 6),
    ('DEPT009', 'Radiology', 6),
    ('DEPT010', 'Anesthesiology', 6),
    ('DEPT011', 'Obstetrics', 6),
    ('DEPT012', 'Gastroenterology', 6),
    ('DEPT013', 'Dermatology', 5),
    ('DEPT014', 'Urology', 5),
    ('DEPT015', 'Nephrology', 5),
    ('DEPT016', 'Pulmonology', 6)
]

FIRST_NAMES = [
    'Sarah', 'Michael', 'Emily', 'David', 'Lisa', 'Robert', 'Jennifer', 'Christopher',
    'Amanda', 'James', 'Michelle', 'Thomas', 'Rachel', 'Daniel', 'Jessica', 'John',
    'Mary', 'William', 'Patricia', 'Richard', 'Linda', 'Joseph', 'Barbara', 'Charles',
    'Elizabeth', 'Steven', 'Susan', 'Matthew', 'Karen', 'Anthony', 'Nancy', 'Mark',
    'Betty', 'Donald', 'Margaret', 'Paul', 'Sandra', 'Andrew', 'Ashley', 'Joshua',
    'Kevin', 'Kimberly', 'Brian', 'Dorothy', 'George', 'Melissa', 'Edward', 'Deborah',
    'Ronald', 'Stephanie', 'Timothy', 'Rebecca', 'Jason', 'Sharon', 'Jeffrey', 'Laura',
    'Ryan', 'Cynthia', 'Jacob', 'Kathleen', 'Gary', 'Amy', 'Nicholas', 'Shirley',
    'Eric', 'Angela', 'Jonathan', 'Helen', 'Stephen', 'Anna', 'Larry', 'Brenda',
    'Justin', 'Pamela', 'Scott', 'Nicole', 'Brandon', 'Emma', 'Benjamin', 'Samantha',
    'Samuel', 'Katherine', 'Raymond', 'Christine', 'Frank', 'Debra', 'Gregory', 'Janet',
    'Alexander', 'Catherine', 'Patrick', 'Carolyn', 'Jack', 'Ruth', 'Dennis', 'Virginia',
    'Jerry', 'Maria', 'Tyler', 'Heather'
]

LAST_NAMES = [
    'Johnson', 'Chen', 'Rodriguez', 'Kim', 'Thompson', 'Wilson', 'Davis', 'Brown',
    'Garcia', 'Miller', 'Lee', 'Anderson', 'White', 'Martinez', 'Taylor', 'Smith',
    'Williams', 'Jones', 'Moore', 'Jackson', 'Martin', 'Perez', 'Harris', 'Clark',
    'Lewis', 'Robinson', 'Walker', 'Young', 'Hall', 'Allen', 'King', 'Wright',
    'Scott', 'Torres', 'Nguyen', 'Hill', 'Green', 'Adams', 'Baker', 'Nelson',
    'Carter', 'Mitchell', 'Roberts', 'Turner', 'Phillips', 'Campbell', 'Parker', 'Evans',
    'Edwards', 'Collins', 'Stewart', 'Morris', 'Rogers', 'Reed', 'Cook', 'Bell',
    'Cooper', 'Richardson', 'Cox', 'Howard', 'Ward', 'Peterson', 'Gray', 'James',
    'Watson', 'Brooks', 'Kelly', 'Sanders', 'Price', 'Bennett', 'Wood', 'Barnes',
    'Ross', 'Henderson', 'Coleman', 'Jenkins', 'Perry', 'Powell', 'Long', 'Patterson',
    'Hughes', 'Flores', 'Washington', 'Butler', 'Simmons', 'Foster', 'Gonzales', 'Bryant',
    'Alexander', 'Russell', 'Griffin', 'Diaz', 'Hayes', 'Myers', 'Ford', 'Hamilton',
    'Graham', 'Sullivan', 'Wallace', 'Woods'
]

HOSPITALS = [
    'City General Hospital',
    'St. Mary\'s Medical Center',
    'University Health System',
    'Memorial Hospital',
    'Regional Medical Center',
    'Community Health Hospital',
    'Metropolitan Medical Center',
    'Riverside Hospital'
]

# Generate 100 physicians
physicians = []
phy_index = 0

for dept_id, dept_name, count in DEPARTMENTS:
    for i in range(count):
        phy_id = f"PHY{phy_index:03d}"
        first_name = FIRST_NAMES[phy_index % len(FIRST_NAMES)]
        last_name = LAST_NAMES[phy_index % len(LAST_NAMES)]
        hospital = HOSPITALS[phy_index % len(HOSPITALS)]
        
        physicians.append({
            'physician_id': phy_id,
            'physician_name': f"Dr. {first_name} {last_name}",
            'first_name': first_name,
            'last_name': last_name,
            'specialty': dept_name,
            'department_id': dept_id,
            'hospital': hospital
        })
        
        phy_index += 1

print(f"Generated {len(physicians)} physicians across {len(DEPARTMENTS)} departments")

# Generate physician performance data for 2022-2024
physician_data = []
YEARS = [2022, 2023, 2024]

for phy in physicians:
    for year in YEARS:
        for month in range(1, 13):
            patients = random.randint(12, 48)
            avg_los = round(random.uniform(2.0, 8.0), 1)
            satisfaction = round(random.uniform(3.6, 5.0), 1)
            complication_rate = round(random.uniform(0.05, 0.19), 3)
            readmission_rate = round(random.uniform(0.10, 0.24), 3)
            revenue = random.randint(6000, 24000)
            
            physician_data.append({
                'physician_id': phy['physician_id'],
                'physician_name': phy['physician_name'],
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

# Write physician performance CSV to both locations
for location in ['data', 'healthcare-website/data']:
    with open(f'{location}/physician_performance.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['physician_id', 'physician_name', 'month', 'year',
                                                'total_patients', 'avg_length_of_stay',
                                                'avg_satisfaction_score', 'complication_rate',
                                                'readmission_rate', 'avg_revenue'])
        writer.writeheader()
        writer.writerows(physician_data)

print(f"\n✓ Physician performance files updated in both locations")

# Write physician registry for reference
with open('physician_registry.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['physician_id', 'physician_name', 'first_name', 
                                            'last_name', 'specialty', 'department_id', 'hospital'])
    writer.writeheader()
    writer.writerows(physicians)

print(f"✓ Created physician_registry.csv with all 100 physicians")

print(f"\n=== SUMMARY ===")
print(f"Total Physicians: {len(physicians)}")
print(f"Performance Records: {len(physician_data)} (100 physicians × 12 months × 3 years)")
print(f"Years: 2022-2024")
print(f"Hospitals: {len(HOSPITALS)}")
print(f"\nPhysician Distribution by Department:")
for dept_id, dept_name, count in DEPARTMENTS:
    dept_phys = [p for p in physicians if p['department_id'] == dept_id]
    print(f"  {dept_name}: {len(dept_phys)} physicians")
