from backend.models import db
from datetime import datetime


class LabTest(db.Model):
    __tablename__ = 'lab_tests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True)
    test_type = db.Column(db.Enum('Blood', 'Urine', 'X-Ray', 'MRI', 'CT Scan', 'ECG', 'Other'), nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    result = db.Column(db.Text)
    report_file = db.Column(db.String(255))
    ordered_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed_date = db.Column(db.DateTime)
    status = db.Column(db.Enum('pending', 'in_progress', 'completed'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship('Patient', backref='lab_tests', lazy=True)
    doctor = db.relationship('Doctor', backref='lab_tests', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': f'{self.patient.first_name} {self.patient.last_name}' if self.patient else None,
            'doctor_id': self.doctor_id,
            'doctor_name': f'{self.doctor.first_name} {self.doctor.last_name}' if self.doctor else None,
            'test_type': self.test_type,
            'test_name': self.test_name,
            'description': self.description,
            'result': self.result,
            'report_file': self.report_file,
            'ordered_date': self.ordered_date.isoformat() if self.ordered_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'status': self.status
        }
