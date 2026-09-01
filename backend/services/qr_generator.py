import qrcode
import os
from backend.config import Config


def generate_patient_qr(patient):
    qr_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'qrcodes')
    os.makedirs(qr_dir, exist_ok=True)

    qr_data = f"Patient ID: {patient.id}\nName: {patient.first_name} {patient.last_name}\nPhone: {patient.phone}"

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    filename = f"patient_{patient.id}.png"
    filepath = os.path.join(qr_dir, filename)
    img.save(filepath)

    return f"assets/qrcodes/{filename}"
