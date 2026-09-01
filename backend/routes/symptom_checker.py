from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.middleware.auth_middleware import staff_required
from backend.services.ai_symptom_checker import check_symptoms_api

symptom_bp = Blueprint('symptom_checker', __name__)


@symptom_bp.route('', methods=['POST'])
@jwt_required()
@staff_required
def check_symptoms():
    data = request.get_json()
    if not data or not data.get('symptoms'):
        return jsonify({'error': 'Symptoms description is required'}), 400

    result = check_symptoms_api(data['symptoms'])
    return jsonify(result), 200
