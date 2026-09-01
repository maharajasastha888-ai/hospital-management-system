from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.middleware.auth_middleware import staff_required
from backend.models import db
from backend.models.medicine import Medicine
from backend.models.pharmacy_bill import PharmacyBill
from backend.models.patient import Patient
from datetime import datetime

pharmacy_bp = Blueprint('pharmacy', __name__)


@pharmacy_bp.route('/medicines', methods=['GET'])
@jwt_required()
@staff_required
def get_medicines():
    search = request.args.get('q', '')
    category = request.args.get('category')
    low_stock = request.args.get('low_stock', type=bool)

    query = Medicine.query
    if search:
        query = query.filter(Medicine.name.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)
    if low_stock:
        query = query.filter(Medicine.stock_quantity <= Medicine.reorder_level)

    medicines = query.order_by(Medicine.name).all()
    return jsonify([m.to_dict() for m in medicines]), 200


@pharmacy_bp.route('/medicines', methods=['POST'])
@jwt_required()
@staff_required
def add_medicine():
    data = request.get_json()
    if not data or not data.get('name') or data.get('price') is None:
        return jsonify({'error': 'Medicine name and price are required'}), 400

    medicine = Medicine(
        name=data['name'],
        category=data.get('category'),
        manufacturer=data.get('manufacturer'),
        price=data['price'],
        expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d').date() if data.get('expiry_date') else None,
        stock_quantity=data.get('stock_quantity', 0),
        reorder_level=data.get('reorder_level', 10)
    )
    db.session.add(medicine)
    db.session.commit()
    return jsonify(medicine.to_dict()), 201


@pharmacy_bp.route('/medicines/<int:medicine_id>', methods=['PUT'])
@jwt_required()
@staff_required
def update_medicine(medicine_id):
    medicine = Medicine.query.get_or_404(medicine_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    for field in ['name', 'category', 'manufacturer', 'price',
                  'stock_quantity', 'reorder_level']:
        if field in data:
            setattr(medicine, field, data[field])

    if data.get('expiry_date'):
        medicine.expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()

    db.session.commit()
    return jsonify(medicine.to_dict()), 200


@pharmacy_bp.route('/medicines/<int:medicine_id>', methods=['DELETE'])
@jwt_required()
@staff_required
def delete_medicine(medicine_id):
    medicine = Medicine.query.get_or_404(medicine_id)
    db.session.delete(medicine)
    db.session.commit()
    return jsonify({'message': 'Medicine deleted successfully'}), 200


@pharmacy_bp.route('/bills', methods=['GET'])
@jwt_required()
@staff_required
def get_pharmacy_bills():
    patient_id = request.args.get('patient_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = PharmacyBill.query
    if patient_id:
        query = query.filter_by(patient_id=patient_id)

    total = query.count()
    bills = query.order_by(PharmacyBill.bill_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'bills': [b.to_dict() for b in bills.items],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    }), 200


@pharmacy_bp.route('/bills', methods=['POST'])
@jwt_required()
@staff_required
def create_pharmacy_bill():
    data = request.get_json()
    if not data or not data.get('patient_id') or not data.get('items'):
        return jsonify({'error': 'Patient and items are required'}), 400

    patient = Patient.query.get(data['patient_id'])
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    bills = []
    total = 0
    for item in data['items']:
        medicine = Medicine.query.get(item['medicine_id'])
        if not medicine:
            return jsonify({'error': f'Medicine {item["medicine_id"]} not found'}), 404
        if medicine.stock_quantity < item['quantity']:
            return jsonify({'error': f'Insufficient stock for {medicine.name}'}), 400

        unit_price = medicine.price
        line_total = unit_price * item['quantity']
        total += line_total

        bill = PharmacyBill(
            patient_id=data['patient_id'],
            medicine_id=item['medicine_id'],
            quantity=item['quantity'],
            unit_price=unit_price,
            total_price=line_total,
            status='unpaid'
        )
        bills.append(bill)

        medicine.stock_quantity -= item['quantity']

    db.session.add_all(bills)
    db.session.commit()

    return jsonify({
        'bills': [b.to_dict() for b in bills],
        'total_amount': total
    }), 201
