from backend.models import db
from datetime import datetime


class Bed(db.Model):
    __tablename__ = 'beds'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ward_name = db.Column(db.String(50), nullable=False)
    bed_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Enum('available', 'occupied', 'maintenance'), default='available')
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'ward_name': self.ward_name,
            'bed_number': self.bed_number,
            'status': self.status,
            'department_id': self.department_id
        }
