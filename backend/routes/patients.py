from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.middleware.auth_middleware import reception_required, staff_required
from backend.models import db
from backend.models.patient import Patient
from backend.models.user import User
from backend.services.qr_generator import generate_patient_qr
import bcrypt
from datetime import datetime

patients_bp = Blueprint('patients', __name__)


@patients_bp.route('', methods=['GET'])
@jwt_required()
@staff_required
def get_patients():
    search = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Patient.query
    if search:
        query = query.filter(
            db.or_(
                Patient.first_name.ilike(f'%{search}%'),
                Patient.last_name.ilike(f'%{search}%'),
                Patient.phone.ilike(f'%{search}%'),
                Patient.email.ilike(f'%{search}%')
            )
        )

    total = query.count()
    patients = query.order_by(Patient.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'patients': [p.to_dict() for p in patients.items],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    }), 200


@patients_bp.route('/<int:patient_id>', methods=['GET'])
@jwt_required()
@staff_required
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify(patient.to_dict()), 200


@patients_bp.route('', methods=['POST'])
@jwt_required()
@reception_required
def add_patient():
    data = request.get_json()
    if not data or not data.get('first_name') or not data.get('phone'):
        return jsonify({'error': 'First name and phone are required'}), 400

    patient = Patient(
        first_name=data['first_name'],
        last_name=data.get('last_name', ''),
        dob=datetime.strptime(data['dob'], '%Y-%m-%d').date() if data.get('dob') else None,
        gender=data.get('gender'),
        blood_group=data.get('blood_group'),
        address=data.get('address'),
        phone=data['phone'],
        email=data.get('email'),
        emergency_contact=data.get('emergency_contact'),
        emergency_contact_name=data.get('emergency_contact_name')
    )
    db.session.add(patient)
    db.session.flush()

    patient.qr_code = generate_patient_qr(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201


@patients_bp.route('/<int:patient_id>', methods=['PUT'])
@jwt_required()
@reception_required
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    for field in ['first_name', 'last_name', 'gender', 'blood_group', 'address',
                  'phone', 'email', 'emergency_contact', 'emergency_contact_name']:
        if field in data:
            setattr(patient, field, data[field])

    if data.get('dob'):
        patient.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()

    db.session.commit()
    return jsonify(patient.to_dict()), 200


@patients_bp.route('/<int:patient_id>', methods=['DELETE'])
@jwt_required()
@reception_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient deleted successfully'}), 200


@patients_bp.route('/<int:patient_id>/qr', methods=['GET'])
@jwt_required()
@staff_required
def get_patient_qr(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if patient.qr_code:
        from flask import send_file
        import os
        qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..', '..', patient.qr_code.lstrip('/'))
        if os.path.exists(qr_path):
            return send_file(qr_path, mimetype='image/png')
    return jsonify({'error': 'QR code not found'}), 404
