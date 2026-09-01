from backend.models import db
from datetime import datetime


class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    blood_group = db.Column(db.String(10))
    address = db.Column(db.Text)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    emergency_contact = db.Column(db.String(20))
    emergency_contact_name = db.Column(db.String(80))
    qr_code = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='patient_profile', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f'{self.first_name} {self.last_name}',
            'dob': self.dob.isoformat() if self.dob else None,
            'gender': self.gender,
            'blood_group': self.blood_group,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'emergency_contact': self.emergency_contact,
            'emergency_contact_name': self.emergency_contact_name,
            'qr_code': self.qr_code,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
