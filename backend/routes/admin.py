from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from backend.middleware.auth_middleware import admin_required
from backend.models.patient import Patient
from backend.models.doctor import Doctor
from backend.models.appointment import Appointment
from backend.models.bill import Bill
from backend.models.bed import Bed
from backend.models.medicine import Medicine
from backend.models import db
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def dashboard():
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    today = datetime.utcnow().date()
    today_appointments = Appointment.query.filter(
        db.func.date(Appointment.appointment_date) == today
    ).count()

    total_revenue = db.session.query(db.func.sum(Bill.paid_amount)).scalar() or 0
    available_beds = Bed.query.filter_by(status='available').count()
    low_stock_medicines = Medicine.query.filter(
        Medicine.stock_quantity <= Medicine.reorder_level
    ).count()

    current_month_start = today.replace(day=1)
    monthly_revenue = db.session.query(db.func.sum(Bill.paid_amount)).filter(
        Bill.created_at >= current_month_start
    ).scalar() or 0

    appointments_today = Appointment.query.filter(
        db.func.date(Appointment.appointment_date) == today
    ).all()

    return jsonify({
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'today_appointments': today_appointments,
        'total_revenue': float(total_revenue),
        'available_beds': available_beds,
        'low_stock_medicines': low_stock_medicines,
        'monthly_revenue': float(monthly_revenue),
        'appointments_today': [a.to_dict() for a in appointments_today]
    }), 200


@admin_bp.route('/revenue/monthly', methods=['GET'])
@jwt_required()
@admin_required
def monthly_revenue_chart():
    today = datetime.utcnow().date()
    data = []
    for i in range(6):
        month_start = today.replace(day=1) - timedelta(days=i * 30)
        month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
        revenue = db.session.query(db.func.sum(Bill.paid_amount)).filter(
            Bill.created_at >= month_start,
            Bill.created_at < month_end
        ).scalar() or 0
        data.append({
            'month': month_start.strftime('%B %Y'),
            'revenue': float(revenue)
        })
    return jsonify(data), 200
