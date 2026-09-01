from backend.models import db
from datetime import datetime


class PharmacyBill(db.Model):
    __tablename__ = 'pharmacy_bills'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    bill_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('paid', 'unpaid'), default='unpaid')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='pharmacy_bills', lazy=True)
    medicine = db.relationship('Medicine', backref='pharmacy_bills', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': f'{self.patient.first_name} {self.patient.last_name}' if self.patient else None,
            'medicine_id': self.medicine_id,
            'medicine_name': self.medicine.name if self.medicine else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'bill_date': self.bill_date.isoformat() if self.bill_date else None,
            'status': self.status
        }
