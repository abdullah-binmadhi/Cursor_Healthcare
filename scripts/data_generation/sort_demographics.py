import csv

# Define age group order
age_order = ['0-17', '18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
age_rank = {age: i for i, age in enumerate(age_order)}

# Read the CSV
data = []
with open('data/patient_demographics.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

# Sort by age group, then gender, then insurance type
data.sort(key=lambda x: (
    age_rank.get(x['age_group'], 999),
    x['gender'],
    x['insurance_type']
))

# Write sorted data
with open('data/patient_demographics.csv', 'w', newline='') as f:
    fieldnames = ['age_group', 'gender', 'insurance_type', 'patient_count', 'avg_length_of_stay', 'avg_cost', 'readmission_rate']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Sorted {len(data)} rows by age group, gender, and insurance type")
