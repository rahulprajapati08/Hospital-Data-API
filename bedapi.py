import random
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Define a list of public hospitals in Delhi
hospitals = [
    {'name': 'AIIMS', 'total_beds': 1000},
    {'name': 'Safdarjung', 'total_beds': 850},
    {'name': 'Lok Nayak Hospital', 'total_beds': 700},
    {'name': 'Ram Manohar Lohia Hospital', 'total_beds': 600},
]

# Define departments common to these hospitals
departments = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'General Surgery', 'Oncology']

# Function to simulate department data without duplicates
def simulate_department_data(department_list):
    random.shuffle(department_list)
    department_stats = []
    for department in department_list:
        department_stats.append({
            'department': department,
            'opd_visits': random.randint(50, 200),
            'admissions': random.randint(10, 50),
            'discharges': random.randint(5, 40),
            'emergency_visits': random.randint(10, 80),
        })
    return department_stats

# Function to simulate hourly data
def simulate_hourly_data():
    return {
        'hour': random.randint(0, 23),
        'emergency_visits': random.randint(20, 100),
        'opd_visits': random.randint(30, 150),
        'admissions': random.randint(5, 30),
    }

# API route to get data for all hospitals
@app.route('/api/hospitals', methods=['GET'])
def get_hospitals_data():
    hospitals_data = []
    for hospital in hospitals:
        # Simulate data for each hospital
        available_beds = random.randint(0, hospital['total_beds'])
        
        # Generate unique department stats for each hospital
        department_stats = simulate_department_data(departments.copy())
        
        # Simulate hourly data for 24 hours
        hourly_stats = [simulate_hourly_data() for _ in range(24)]
        
        hospitals_data.append({
            'name': hospital['name'],
            'total_beds': hospital['total_beds'],
            'available_beds': available_beds,
            'department_stats': department_stats,
            'hourly_stats': hourly_stats
        })
    
    return jsonify(hospitals_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
