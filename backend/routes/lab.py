from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required
from backend.middleware.auth_middleware import staff_required
from backend.models import db
from backend.models.lab_test import LabTest
from backend.models.patient import Patient
from backend.config import Config
from datetime import datetime
import os

lab_bp = Blueprint('lab', __name__)


@lab_bp.route('/tests', methods=['GET'])
@jwt_required()
@staff_required
def get_lab_tests():
    patient_id = request.args.get('patient_id', type=int)
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = LabTest.query
    if patient_id:
        query = query.filter_by(patient_id=patient_id)
    if status:
        query = query.filter_by(status=status)

    total = query.count()
    tests = query.order_by(LabTest.ordered_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'tests': [t.to_dict() for t in tests.items],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    }), 200


@lab_bp.route('/tests', methods=['POST'])
@jwt_required()
@staff_required
def order_lab_test():
    data = request.get_json()
    if not data or not data.get('patient_id') or not data.get('test_type') or not data.get('test_name'):
        return jsonify({'error': 'Patient, test type, and test name are required'}), 400

    patient = Patient.query.get(data['patient_id'])
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    test = LabTest(
        patient_id=data['patient_id'],
        doctor_id=data.get('doctor_id'),
        test_type=data['test_type'],
        test_name=data['test_name'],
        description=data.get('description', '')
    )
    db.session.add(test)
    db.session.commit()
    return jsonify(test.to_dict()), 201


@lab_bp.route('/tests/<int:test_id>', methods=['GET'])
@jwt_required()
@staff_required
def get_lab_test(test_id):
    test = LabTest.query.get_or_404(test_id)
    return jsonify(test.to_dict()), 200


@lab_bp.route('/tests/<int:test_id>/result', methods=['PUT'])
@jwt_required()
@staff_required
def update_lab_result(test_id):
    test = LabTest.query.get_or_404(test_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if data.get('result') is not None:
        test.result = data['result']
    test.status = data.get('status', test.status)
    if test.status == 'completed' and not test.completed_date:
        test.completed_date = datetime.utcnow()
    db.session.commit()
    return jsonify(test.to_dict()), 200


@lab_bp.route('/tests/<int:test_id>/report', methods=['POST'])
@jwt_required()
@staff_required
def upload_report(test_id):
    test = LabTest.query.get_or_404(test_id)

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    filename = f"lab_report_{test_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{ext}"
    filepath = os.path.join(Config.UPLOAD_FOLDER, 'lab_reports', filename)

    file.save(filepath)
    test.report_file = f'uploads/lab_reports/{filename}'
    test.status = 'completed'
    test.completed_date = datetime.utcnow()
    db.session.commit()

    return jsonify(test.to_dict()), 200


@lab_bp.route('/tests/<int:test_id>/report/download', methods=['GET'])
@jwt_required()
@staff_required
def download_report(test_id):
    test = LabTest.query.get_or_404(test_id)
    if not test.report_file:
        return jsonify({'error': 'No report file'}), 404

    directory = os.path.join(Config.UPLOAD_FOLDER, 'lab_reports')
    filename = os.path.basename(test.report_file)
    return send_from_directory(directory, filename)
