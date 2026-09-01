from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import jsonify
from backend.models.user import User


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            if user.role not in roles:
                return jsonify({'error': 'Access denied: insufficient permissions'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(fn):
    return role_required('admin')(fn)


def doctor_required(fn):
    return role_required('admin', 'doctor')(fn)


def reception_required(fn):
    return role_required('admin', 'receptionist')(fn)


def staff_required(fn):
    return role_required('admin', 'doctor', 'receptionist', 'pharmacist', 'lab_technician')(fn)
