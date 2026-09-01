from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.middleware.auth_middleware import admin_required, staff_required
from backend.models import db
from backend.models.doctor import Doctor
from backend.models.user import User
import bcrypt
from datetime import datetime

doctors_bp = Blueprint('doctors', __name__)


@doctors_bp.route('', methods=['GET'])
@jwt_required()
@staff_required
def get_doctors():
    department_id = request.args.get('department_id', type=int)
    query = Doctor.query.filter_by(is_available=True)
    if department_id:
        query = query.filter_by(department_id=department_id)
    doctors = query.all()
    return jsonify([d.to_dict() for d in doctors]), 200


@doctors_bp.route('/<int:doctor_id>', methods=['GET'])
@jwt_required()
@staff_required
def get_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify(doctor.to_dict()), 200


@doctors_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
def add_doctor():
    data = request.get_json()
    if not data or not data.get('first_name') or not data.get('last_name'):
        return jsonify({'error': 'First name and last name are required'}), 400

    user = User(
        username=data.get('email', f"dr_{data['first_name'].lower()}_{data['last_name'].lower()}"),
        email=data.get('email', ''),
        password_hash=bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        role='doctor',
        phone=data.get('phone')
    )
    db.session.add(user)
    db.session.flush()

    doctor = Doctor(
        user_id=user.id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        specialization=data.get('specialization'),
        department_id=data.get('department_id'),
        qualification=data.get('qualification'),
        schedule=data.get('schedule', {}),
        fee=data.get('fee', 0.0),
        phone=data.get('phone'),
        email=data.get('email')
    )
    db.session.add(doctor)
    db.session.commit()
    return jsonify(doctor.to_dict()), 201


@doctors_bp.route('/<int:doctor_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    for field in ['first_name', 'last_name', 'specialization', 'department_id',
                  'qualification', 'schedule', 'fee', 'phone', 'email', 'is_available']:
        if field in data:
            setattr(doctor, field, data[field])

    db.session.commit()
    return jsonify(doctor.to_dict()), 200


@doctors_bp.route('/<int:doctor_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if doctor.user_id:
        user = User.query.get(doctor.user_id)
        if user:
            db.session.delete(user)
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted successfully'}), 200


@doctors_bp.route('/available', methods=['GET'])
@jwt_required()
@staff_required
def get_available_doctors():
    date_str = request.args.get('date')
    department_id = request.args.get('department_id', type=int)

    query = Doctor.query.filter_by(is_available=True)
    if department_id:
        query = query.filter_by(department_id=department_id)

    doctors = query.all()
    result = []
    for doctor in doctors:
        schedule = doctor.schedule or {}
        day_name = datetime.strptime(date_str, '%Y-%m-%d').strftime('%A') if date_str else ''
        day_slots = schedule.get(day_name.lower(), [])
        result.append({
            **doctor.to_dict(),
            'available_slots': day_slots
        })
    return jsonify(result), 200
