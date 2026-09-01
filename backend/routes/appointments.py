from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.middleware.auth_middleware import reception_required, staff_required
from backend.models import db
from backend.models.appointment import Appointment
from backend.models.patient import Patient
from backend.models.doctor import Doctor
from backend.models.user import User
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)


@appointments_bp.route('', methods=['GET'])
@jwt_required()
@staff_required
def get_appointments():
    date_str = request.args.get('date')
    doctor_id = request.args.get('doctor_id', type=int)
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Appointment.query

    if date_str:
        query = query.filter(db.func.date(Appointment.appointment_date) ==
                             datetime.strptime(date_str, '%Y-%m-%d').date())
    if doctor_id:
        query = query.filter_by(doctor_id=doctor_id)
    if status:
        query = query.filter_by(status=status)

    total = query.count()
    appointments = query.order_by(Appointment.appointment_date.desc(),
                                  Appointment.time_slot.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'appointments': [a.to_dict() for a in appointments.items],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    }), 200


@appointments_bp.route('', methods=['POST'])
@jwt_required()
@reception_required
def book_appointment():
    data = request.get_json()
    if not data or not data.get('patient_id') or not data.get('doctor_id') \
            or not data.get('appointment_date') or not data.get('time_slot'):
        return jsonify({'error': 'Patient, doctor, date, and time slot are required'}), 400

    patient = Patient.query.get(data['patient_id'])
    doctor = Doctor.query.get(data['doctor_id'])
    if not patient or not doctor:
        return jsonify({'error': 'Patient or doctor not found'}), 404

    existing = Appointment.query.filter_by(
        doctor_id=data['doctor_id'],
        appointment_date=datetime.strptime(data['appointment_date'], '%Y-%m-%d').date(),
        time_slot=data['time_slot'],
        status='scheduled'
    ).first()
    if existing:
        return jsonify({'error': 'Time slot already booked'}), 409

    appointment = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        appointment_date=datetime.strptime(data['appointment_date'], '%Y-%m-%d').date(),
        time_slot=data['time_slot'],
        reason=data.get('reason', '')
    )
    db.session.add(appointment)
    db.session.commit()

    return jsonify(appointment.to_dict()), 201


@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
@jwt_required()
@staff_required
def get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify(appointment.to_dict()), 200


@appointments_bp.route('/<int:appointment_id>/cancel', methods=['PUT'])
@jwt_required()
@reception_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'cancelled'
    db.session.commit()
    return jsonify(appointment.to_dict()), 200


@appointments_bp.route('/<int:appointment_id>/complete', methods=['PUT'])
@jwt_required()
@staff_required
def complete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'completed'
    db.session.commit()
    return jsonify(appointment.to_dict()), 200
