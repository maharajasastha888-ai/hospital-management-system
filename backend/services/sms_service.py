import logging
import os

logger = logging.getLogger(__name__)


def send_sms(phone_number, message):
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
    twilio_token = os.getenv('TWILIO_AUTH_TOKEN', '')
    twilio_phone = os.getenv('TWILIO_PHONE_NUMBER', '')

    if not twilio_sid or not twilio_token or not twilio_phone:
        logger.warning('SMS not configured. Skipping SMS send.')
        return False

    try:
        from twilio.rest import Client
        client = Client(twilio_sid, twilio_token)
        client.messages.create(
            body=message,
            from_=twilio_phone,
            to=phone_number
        )
        logger.info(f'SMS sent to {phone_number}')
        return True
    except ImportError:
        logger.warning('Twilio package not installed. Skipping SMS.')
        return False
    except Exception as e:
        logger.error(f'Failed to send SMS: {str(e)}')
        return False


def send_appointment_sms(phone_number, patient_name, doctor_name, date, time_slot):
    message = f'Dear {patient_name}, your appointment with Dr. {doctor_name} on {date} at {time_slot} is confirmed. - HMS'
    return send_sms(phone_number, message)
