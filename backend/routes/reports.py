from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.middleware.auth_middleware import admin_required
from backend.models import db
from backend.models.patient import Patient
from backend.models.doctor import Doctor
from backend.models.appointment import Appointment
from backend.models.bill import Bill
from backend.models.lab_test import LabTest
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/daily-patients', methods=['GET'])
@jwt_required()
@admin_required
def daily_patients():
    date_str = request.args.get('date', datetime.utcnow().strftime('%Y-%m-%d'))
    report_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    total_appointments = Appointment.query.filter(
        db.func.date(Appointment.appointment_date) == report_date
    ).count()

    completed = Appointment.query.filter(
        db.func.date(Appointment.appointment_date) == report_date,
        Appointment.status == 'completed'
    ).count()

    cancelled = Appointment.query.filter(
        db.func.date(Appointment.appointment_date) == report_date,
        Appointment.status == 'cancelled'
    ).count()

    revenue = db.session.query(db.func.sum(Bill.paid_amount)).filter(
        db.func.date(Bill.created_at) == report_date
    ).scalar() or 0

    new_patients = Patient.query.filter(
        db.func.date(Patient.created_at) == report_date
    ).count()

    appointments = Appointment.query.filter(
        db.func.date(Appointment.appointment_date) == report_date
    ).order_by(Appointment.time_slot).all()

    return jsonify({
        'date': date_str,
        'total_appointments': total_appointments,
        'completed': completed,
        'cancelled': cancelled,
        'revenue': float(revenue),
        'new_patients': new_patients,
        'appointments': [a.to_dict() for a in appointments]
    }), 200


@reports_bp.route('/monthly-revenue', methods=['GET'])
@jwt_required()
@admin_required
def monthly_revenue():
    year = request.args.get('year', datetime.utcnow().year, type=int)

    monthly_data = []
    for month in range(1, 13):
        total_revenue = db.session.query(db.func.sum(Bill.paid_amount)).filter(
            db.extract('year', Bill.created_at) == year,
            db.extract('month', Bill.created_at) == month
        ).scalar() or 0

        total_bills = Bill.query.filter(
            db.extract('year', Bill.created_at) == year,
            db.extract('month', Bill.created_at) == month
        ).count()

        monthly_data.append({
            'month': month,
            'month_name': datetime(year, month, 1).strftime('%B'),
            'revenue': float(total_revenue),
            'total_bills': total_bills
        })

    total_yearly = sum(m['revenue'] for m in monthly_data)
    return jsonify({
        'year': year,
        'monthly_data': monthly_data,
        'total_yearly': total_yearly
    }), 200


@reports_bp.route('/doctors', methods=['GET'])
@jwt_required()
@admin_required
def doctor_report():
    date_from = request.args.get('from')
    date_to = request.args.get('to')

    query = Appointment.query
    if date_from:
        query = query.filter(Appointment.appointment_date >=
                             datetime.strptime(date_from, '%Y-%m-%d').date())
    if date_to:
        query = query.filter(Appointment.appointment_date <=
                             datetime.strptime(date_to, '%Y-%m-%d').date())

    doctors = Doctor.query.all()
    report = []
    for doctor in doctors:
        doc_appointments = query.filter_by(doctor_id=doctor.id)
        total = doc_appointments.count()
        completed = doc_appointments.filter_by(status='completed').count()
        cancelled = doc_appointments.filter_by(status='cancelled').count()

        report.append({
            'doctor_id': doctor.id,
            'doctor_name': f'{doctor.first_name} {doctor.last_name}',
            'specialization': doctor.specialization,
            'total_appointments': total,
            'completed': completed,
            'cancelled': cancelled,
            'completion_rate': round((completed / total * 100) if total > 0 else 0, 2)
        })

    return jsonify(report), 200
