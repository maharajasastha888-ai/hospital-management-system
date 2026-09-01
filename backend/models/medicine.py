from backend.models import db
from datetime import datetime


class Medicine(db.Model):
    __tablename__ = 'medicines'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    manufacturer = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False, default=0.0)
    expiry_date = db.Column(db.Date)
    stock_quantity = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'manufacturer': self.manufacturer,
            'price': self.price,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'stock_quantity': self.stock_quantity,
            'reorder_level': self.reorder_level,
            'low_stock': self.stock_quantity <= self.reorder_level
        }
