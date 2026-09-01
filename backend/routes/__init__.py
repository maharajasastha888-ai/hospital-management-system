from backend.routes.auth import auth_bp
from backend.routes.admin import admin_bp
from backend.routes.patients import patients_bp
from backend.routes.doctors import doctors_bp
from backend.routes.appointments import appointments_bp
from backend.routes.departments import departments_bp
from backend.routes.lab import lab_bp
from backend.routes.pharmacy import pharmacy_bp
from backend.routes.billing import billing_bp
from backend.routes.reports import reports_bp
from backend.routes.symptom_checker import symptom_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(patients_bp, url_prefix='/api/patients')
    app.register_blueprint(doctors_bp, url_prefix='/api/doctors')
    app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
    app.register_blueprint(departments_bp, url_prefix='/api/departments')
    app.register_blueprint(lab_bp, url_prefix='/api/lab')
    app.register_blueprint(pharmacy_bp, url_prefix='/api/pharmacy')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(symptom_bp, url_prefix='/api/symptom-checker')
