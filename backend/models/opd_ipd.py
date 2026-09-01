from backend.models import db
from datetime import datetime


class OPDIPD(db.Model):
    __tablename__ = 'opd_ipd'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    type = db.Column(db.Enum('OPD', 'IPD'), nullable=False)
    admission_date = db.Column(db.DateTime, nullable=False)
    discharge_date = db.Column(db.DateTime)
    bed_id = db.Column(db.Integer, db.ForeignKey('beds.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    diagnosis = db.Column(db.Text)
    status = db.Column(db.Enum('active', 'discharged'), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='opd_ipd_records', lazy=True)
    bed = db.relationship('Bed', backref='opd_ipd_records', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': f'{self.patient.first_name} {self.patient.last_name}' if self.patient else None,
            'type': self.type,
            'admission_date': self.admission_date.isoformat() if self.admission_date else None,
            'discharge_date': self.discharge_date.isoformat() if self.discharge_date else None,
            'bed_id': self.bed_id,
            'bed_info': f'{self.bed.ward_name} - {self.bed.bed_number}' if self.bed else None,
            'department_id': self.department_id,
            'diagnosis': self.diagnosis,
            'status': self.status
        }
