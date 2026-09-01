from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.middleware.auth_middleware import staff_required
from backend.models import db
from backend.models.bill import Bill
from backend.models.payment import Payment
from backend.models.patient import Patient
from backend.models.appointment import Appointment
from backend.services.pdf_generator import generate_invoice_pdf
from datetime import datetime
import random
import string

billing_bp = Blueprint('billing', __name__)


def generate_invoice_number():
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f'INV-{timestamp}-{rand}'


@billing_bp.route('/bills', methods=['GET'])
@jwt_required()
@staff_required
def get_bills():
    patient_id = request.args.get('patient_id', type=int)
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = Bill.query
    if patient_id:
        query = query.filter_by(patient_id=patient_id)
    if status:
        query = query.filter_by(status=status)

    total = query.count()
    bills = query.order_by(Bill.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'bills': [b.to_dict() for b in bills.items],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    }), 200


@billing_bp.route('/bills', methods=['POST'])
@jwt_required()
@staff_required
def create_bill():
    data = request.get_json()
    if not data or not data.get('patient_id'):
        return jsonify({'error': 'Patient is required'}), 400

    patient = Patient.query.get(data['patient_id'])
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    consultation_fee = data.get('consultation_fee', 0)
    lab_fee = data.get('lab_fee', 0)
    medicine_fee = data.get('medicine_fee', 0)
    other_fee = data.get('other_fee', 0)
    total_amount = consultation_fee + lab_fee + medicine_fee + other_fee

    bill = Bill(
        patient_id=data['patient_id'],
        appointment_id=data.get('appointment_id'),
        consultation_fee=consultation_fee,
        lab_fee=lab_fee,
        medicine_fee=medicine_fee,
        other_fee=other_fee,
        total_amount=total_amount,
        paid_amount=0,
        due_amount=total_amount,
        status='unpaid',
        invoice_number=generate_invoice_number()
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify(bill.to_dict()), 201


@billing_bp.route('/bills/<int:bill_id>', methods=['GET'])
@jwt_required()
@staff_required
def get_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    return jsonify(bill.to_dict()), 200


@billing_bp.route('/bills/<int:bill_id>/pay', methods=['POST'])
@jwt_required()
@staff_required
def make_payment(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    data = request.get_json()
    if not data or not data.get('amount') or not data.get('payment_method'):
        return jsonify({'error': 'Amount and payment method are required'}), 400

    amount = data['amount']
    if amount <= 0:
        return jsonify({'error': 'Amount must be positive'}), 400

    payment = Payment(
        bill_id=bill_id,
        amount=amount,
        payment_method=data['payment_method'],
        transaction_id=data.get('transaction_id', ''),
        notes=data.get('notes', '')
    )
    db.session.add(payment)

    bill.paid_amount += amount
    bill.due_amount = bill.total_amount - bill.paid_amount
    if bill.due_amount <= 0:
        bill.status = 'paid'
        bill.due_amount = 0
    elif bill.paid_amount > 0:
        bill.status = 'partial'

    db.session.commit()
    return jsonify({
        'bill': bill.to_dict(),
        'payment': payment.to_dict()
    }), 200


@billing_bp.route('/bills/<int:bill_id>/pdf', methods=['GET'])
@jwt_required()
@staff_required
def download_bill_pdf(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    pdf_buffer = generate_invoice_pdf(bill)
    from flask import send_file
    import io
    return send_file(
        io.BytesIO(pdf_buffer),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'invoice_{bill.invoice_number}.pdf'
    )
