from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from backend.models.user import User
from backend.models.patient import Patient
from backend.models.doctor import Doctor
from backend.models.department import Department
from backend.models.appointment import Appointment
from backend.models.medicine import Medicine
from backend.models.pharmacy_bill import PharmacyBill
from backend.models.lab_test import LabTest
from backend.models.bill import Bill
from backend.models.payment import Payment
from backend.models.bed import Bed
from backend.models.opd_ipd import OPDIPD
