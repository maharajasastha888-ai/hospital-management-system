from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.middleware.auth_middleware import admin_required, staff_required
from backend.models import db
from backend.models.department import Department

departments_bp = Blueprint('departments', __name__)


@departments_bp.route('', methods=['GET'])
@jwt_required()
@staff_required
def get_departments():
    departments = Department.query.all()
    return jsonify([d.to_dict() for d in departments]), 200


@departments_bp.route('/<int:dept_id>', methods=['GET'])
@jwt_required()
@staff_required
def get_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    return jsonify(department.to_dict()), 200


@departments_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
def add_department():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Department name is required'}), 400

    existing = Department.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Department already exists'}), 409

    department = Department(
        name=data['name'],
        description=data.get('description', ''),
        head_doctor_id=data.get('head_doctor_id')
    )
    db.session.add(department)
    db.session.commit()
    return jsonify(department.to_dict()), 201


@departments_bp.route('/<int:dept_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if data.get('name'):
        department.name = data['name']
    if data.get('description') is not None:
        department.description = data['description']
    if data.get('head_doctor_id') is not None:
        department.head_doctor_id = data['head_doctor_id']

    db.session.commit()
    return jsonify(department.to_dict()), 200


@departments_bp.route('/<int:dept_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    db.session.delete(department)
    db.session.commit()
    return jsonify({'message': 'Department deleted successfully'}), 200
