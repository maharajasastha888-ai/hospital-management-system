from backend.models import db
from datetime import datetime


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    specialization = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    qualification = db.Column(db.String(200))
    schedule = db.Column(db.JSON)
    fee = db.Column(db.Float, default=0.0)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    department = db.relationship('Department', backref='doctors', lazy=True,
                                 foreign_keys=[department_id])
    user = db.relationship('User', backref='doctor_profile', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f'{self.first_name} {self.last_name}',
            'specialization': self.specialization,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'qualification': self.qualification,
            'schedule': self.schedule,
            'fee': self.fee,
            'phone': self.phone,
            'email': self.email,
            'is_available': self.is_available
        }
