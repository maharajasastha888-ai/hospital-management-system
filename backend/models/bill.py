from backend.models import db
from datetime import datetime


class Bill(db.Model):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    opd_ipd_id = db.Column(db.Integer, db.ForeignKey('opd_ipd.id'))
    consultation_fee = db.Column(db.Float, default=0.0)
    lab_fee = db.Column(db.Float, default=0.0)
    medicine_fee = db.Column(db.Float, default=0.0)
    other_fee = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, default=0.0)
    due_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.Enum('unpaid', 'partial', 'paid'), default='unpaid')
    invoice_number = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', backref='bills', lazy=True)
    appointment = db.relationship('Appointment', backref='bill', lazy=True)
    payments = db.relationship('Payment', backref='bill', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': f'{self.patient.first_name} {self.patient.last_name}' if self.patient else None,
            'appointment_id': self.appointment_id,
            'consultation_fee': self.consultation_fee,
            'lab_fee': self.lab_fee,
            'medicine_fee': self.medicine_fee,
            'other_fee': self.other_fee,
            'total_amount': self.total_amount,
            'paid_amount': self.paid_amount,
            'due_amount': self.due_amount,
            'status': self.status,
            'invoice_number': self.invoice_number,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
