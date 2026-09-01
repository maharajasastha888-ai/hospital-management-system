import re


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    pattern = r'^\+?1?\d{10,15}$'
    return re.match(pattern, phone) is not None


def validate_password(password):
    if len(password) < 6:
        return False, 'Password must be at least 6 characters'
    return True, ''


def sanitize_string(value):
    if value is None:
        return ''
    return str(value).strip()
