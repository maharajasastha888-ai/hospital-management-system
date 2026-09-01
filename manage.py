"""
Management script for Hospital Management System.
Usage: python manage.py [command]

Commands:
  init_db     - Create all database tables
  seed        - Seed database with initial data
  reset       - Drop all tables and re-create + seed
  create-admin - Create an admin user
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.models import db
from backend.models.user import User
from backend.models.department import Department
from backend.models.doctor import Doctor
from backend.models.bed import Bed
from backend.models.medicine import Medicine
import bcrypt
from datetime import datetime, timedelta


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print('Database tables created successfully!')


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        if User.query.first():
            print('Database already seeded. Use "reset" to re-seed.')
            return

        hashed_admin = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        hashed_pass = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        users = [
            User(username='admin', email='admin@hospital.com', password_hash=hashed_admin,
                 role='admin', phone='1234567890', is_active=True),
            User(username='doctor1', email='doctor1@hospital.com', password_hash=hashed_pass,
                 role='doctor', phone='1234567891', is_active=True),
            User(username='reception', email='reception@hospital.com', password_hash=hashed_pass,
                 role='receptionist', phone='1234567892', is_active=True),
            User(username='pharmacist', email='pharmacist@hospital.com', password_hash=hashed_pass,
                 role='pharmacist', phone='1234567893', is_active=True),
            User(username='labtech', email='labtech@hospital.com', password_hash=hashed_pass,
                 role='lab_technician', phone='1234567894', is_active=True),
            User(username='patient1', email='patient1@example.com', password_hash=hashed_pass,
                 role='patient', phone='9876543210', is_active=True),
        ]
        db.session.add_all(users)
        db.session.flush()

        departments = [
            Department(name='General Medicine', description='General medical consultations and treatment'),
            Department(name='Cardiology', description='Heart and cardiovascular system'),
            Department(name='Neurology', description='Brain and nervous system'),
            Department(name='Orthopedics', description='Bones and joints'),
            Department(name='Pediatrics', description='Child healthcare'),
            Department(name='Gynecology', description="Women's health"),
            Department(name='Dermatology', description='Skin care'),
            Department(name='Ophthalmology', description='Eye care'),
            Department(name='ENT', description='Ear, Nose, Throat'),
        ]
        db.session.add_all(departments)
        db.session.flush()

        doctors = [
            Doctor(user_id=2, first_name='Rajesh', last_name='Kumar', specialization='General Physician',
                   department_id=1, qualification='MBBS, MD', fee=500,
                   schedule={'monday': ['09:00 AM', '10:00 AM', '11:00 AM'], 'tuesday': ['09:00 AM', '10:00 AM', '11:00 AM']},
                   phone='1234567891', email='doctor1@hospital.com'),
        ]
        db.session.add_all(doctors)
        db.session.flush()

        beds = []
        for ward in ['General Ward', 'ICU', 'Private']:
            for i in range(1, 11):
                beds.append(Bed(ward_name=ward, bed_number=f'{ward[:3]}-{i:02d}', status='available'))
        db.session.add_all(beds)

        medicines = [
            Medicine(name='Paracetamol', category='Analgesic', manufacturer='ABC Pharma', price=2.50, stock_quantity=500, reorder_level=50),
            Medicine(name='Amoxicillin', category='Antibiotic', manufacturer='XYZ Pharma', price=5.00, stock_quantity=200, reorder_level=30),
            Medicine(name='Omeprazole', category='Antacid', manufacturer='PQR Pharma', price=3.00, stock_quantity=300, reorder_level=40),
            Medicine(name='Cetirizine', category='Antihistamine', manufacturer='LMN Pharma', price=1.50, stock_quantity=150, reorder_level=20),
            Medicine(name='Metformin', category='Diabetes', manufacturer='ABC Pharma', price=4.00, stock_quantity=100, reorder_level=15),
        ]
        db.session.add_all(medicines)

        db.session.commit()
        print('Database seeded successfully!')
        print('')
        print('Login Credentials:')
        print('  Admin:      admin / admin123')
        print('  Doctor:     doctor1 / password123')
        print('  Reception:  reception / password123')
        print('  Pharmacist: pharmacist / password123')
        print('  Lab Tech:   labtech / password123')
        print('  Patient:    patient1 / password123')


def reset():
    app = create_app()
    with app.app_context():
        db.drop_all()
        print('All tables dropped.')
    seed()


def create_admin():
    app = create_app()
    with app.app_context():
        username = input('Username: ')
        email = input('Email: ')
        password = input('Password: ')
        phone = input('Phone: ')

        existing = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing:
            print('User with this username or email already exists.')
            return

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=username, email=email, password_hash=hashed,
                    role='admin', phone=phone, is_active=True)
        db.session.add(user)
        db.session.commit()
        print(f'Admin user "{username}" created successfully!')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1]
    if command == 'init_db':
        init_db()
    elif command == 'seed':
        seed()
    elif command == 'reset':
        reset()
    elif command == 'create-admin':
        create_admin()
    else:
        print(f'Unknown command: {command}')
        print(__doc__)
