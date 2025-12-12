import csv
import random

# Read existing data
existing_data = []
with open('data/physician_performance.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing_data.append(row)

print(f"Current physicians: 15 (180 rows)")

# Generate physician names
first_names = [
    'John', 'Mary', 'Robert', 'Patricia', 'James', 'Jennifer', 'Michael', 'Linda',
    'William', 'Barbara', 'David', 'Elizabeth', 'Richard', 'Susan', 'Joseph', 'Jessica',
    'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
    'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
    'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
    'Kenneth', 'Carol', 'Kevin', 'Amanda', 'Brian', 'Dorothy', 'George', 'Melissa',
    'Edward', 'Deborah', 'Ronald', 'Stephanie', 'Timothy', 'Rebecca', 'Jason', 'Sharon',
    'Jeffrey', 'Laura', 'Ryan', 'Cynthia', 'Jacob', 'Kathleen', 'Gary', 'Amy',
    'Nicholas', 'Shirley', 'Eric', 'Angela', 'Jonathan', 'Helen', 'Stephen', 'Anna',
    'Larry', 'Brenda', 'Justin', 'Pamela', 'Scott', 'Nicole', 'Brandon', 'Emma',
    'Benjamin', 'Samantha', 'Samuel', 'Katherine', 'Raymond', 'Christine'
]

last_names = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
    'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
    'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
    'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
    'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
    'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker',
    'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy',
    'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper', 'Peterson', 'Bailey',
    'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson', 'Watson',
    'Brooks', 'Chavez', 'Wood', 'James', 'Bennett', 'Gray', 'Mendoza', 'Ruiz', 'Hughes'
]

# Generate new physicians data
new_rows = []
physicians_to_add = 85

for i in range(15, 15 + physicians_to_add):
    physician_id = f"PHY{i:03d}"
    physician_name = f"Dr. {random.choice(first_names)} {random.choice(last_names)}"
    
    # Generate 12 months of data for each physician
    for month in range(1, 13):
        total_patients = random.randint(10, 50)
        avg_length_of_stay = round(random.uniform(2.0, 8.0), 1)
        avg_satisfaction_score = round(random.uniform(3.5, 5.0), 1)
        complication_rate = round(random.uniform(0.05, 0.20), 3)
        readmission_rate = round(random.uniform(0.10, 0.25), 3)
        avg_revenue = random.randint(5000, 25000)
        
        new_rows.append({
            'physician_id': physician_id,
            'physician_name': physician_name,
            'month': month,
            'year': 2024,
            'total_patients': total_patients,
            'avg_length_of_stay': avg_length_of_stay,
            'avg_satisfaction_score': avg_satisfaction_score,
            'complication_rate': complication_rate,
            'readmission_rate': readmission_rate,
            'avg_revenue': avg_revenue
        })

# Combine data
all_data = existing_data + new_rows

# Write to CSV
with open('data/physician_performance.csv', 'w', newline='') as f:
    fieldnames = ['physician_id', 'physician_name', 'month', 'year', 'total_patients', 
                  'avg_length_of_stay', 'avg_satisfaction_score', 'complication_rate', 
                  'readmission_rate', 'avg_revenue']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)

print(f"New total physicians: 100 ({len(all_data)} rows)")
print(f"Added {physicians_to_add} physicians ({len(new_rows)} rows)")
