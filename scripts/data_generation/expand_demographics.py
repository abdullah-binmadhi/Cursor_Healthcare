import csv
import random

# Define the data ranges
age_groups = ['0-17', '18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
genders = ['M', 'F']
insurance_types = [
    'Blue Cross Blue Shield', 'Aetna', 'Cigna', 'UnitedHealthcare', 
    'Humana', 'Kaiser Permanente', 'Anthem', 'Medicare', 
    'Medicaid', 'Tricare', 'Health Net', 'Molina Healthcare'
]

# Read existing data
existing_data = []
with open('data/patient_demographics.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing_data.append(row)

print(f"Current rows: {len(existing_data)}")

# Generate new rows to reach 1000 total
new_rows = []
target_rows = 1000
rows_to_add = target_rows - len(existing_data)

for i in range(rows_to_add):
    age_group = random.choice(age_groups)
    gender = random.choice(genders)
    insurance_type = random.choice(insurance_types)
    
    # Generate realistic values
    patient_count = random.randint(50, 300)
    avg_length_of_stay = round(random.uniform(2.0, 8.0), 1)
    avg_cost = random.randint(3000, 12000)
    readmission_rate = round(random.uniform(0.1, 0.25), 3)
    
    new_rows.append({
        'age_group': age_group,
        'gender': gender,
        'insurance_type': insurance_type,
        'patient_count': patient_count,
        'avg_length_of_stay': avg_length_of_stay,
        'avg_cost': avg_cost,
        'readmission_rate': readmission_rate
    })

# Combine and write
all_data = existing_data + new_rows

with open('data/patient_demographics.csv', 'w', newline='') as f:
    fieldnames = ['age_group', 'gender', 'insurance_type', 'patient_count', 'avg_length_of_stay', 'avg_cost', 'readmission_rate']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)

print(f"New total rows: {len(all_data)}")
print(f"Added {rows_to_add} new rows")
