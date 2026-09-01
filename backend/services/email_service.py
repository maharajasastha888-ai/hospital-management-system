from flask_mail import Message
from backend.app import mail
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def send_appointment_confirmation(patient_email, patient_name, doctor_name, date, time_slot):
    if not current_app.config.get('MAIL_USERNAME'):
        logger.warning('Email not configured. Skipping email send.')
        return False

    try:
        msg = Message(
            subject='Appointment Confirmation - Hospital Management System',
            recipients=[patient_email],
            sender=current_app.config['MAIL_USERNAME']
        )
        msg.body = f"""
Dear {patient_name},

Your appointment has been confirmed.

Doctor: Dr. {doctor_name}
Date: {date}
Time: {time_slot}

Please arrive 15 minutes before your scheduled time.

For any changes or cancellations, please contact the reception.

Thank you,
Hospital Management System
        """
        mail.send(msg)
        logger.info(f'Appointment confirmation sent to {patient_email}')
        return True
    except Exception as e:
        logger.error(f'Failed to send email: {str(e)}')
        return False


def send_bill_email(patient_email, patient_name, invoice_number, total_amount):
    if not current_app.config.get('MAIL_USERNAME'):
        logger.warning('Email not configured. Skipping email send.')
        return False

    try:
        msg = Message(
            subject=f'Invoice #{invoice_number} - Hospital Management System',
            recipients=[patient_email],
            sender=current_app.config['MAIL_USERNAME']
        )
        msg.body = f"""
Dear {patient_name},

Please find your invoice details below:

Invoice Number: {invoice_number}
Total Amount: ${total_amount:.2f}

Thank you for choosing our hospital.

Regards,
Hospital Management System
        """
        mail.send(msg)
        return True
    except Exception as e:
        logger.error(f'Failed to send bill email: {str(e)}')
        return False
