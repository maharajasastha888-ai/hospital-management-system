import logging
import os
import json

logger = logging.getLogger(__name__)

SYMPTOM_DATABASE = {
    'fever': {'possible_conditions': ['Common Cold', 'Flu', 'Infection', 'COVID-19'], 'department': 'General Medicine'},
    'headache': {'possible_conditions': ['Migraine', 'Tension Headache', 'Sinusitis'], 'department': 'Neurology'},
    'chest pain': {'possible_conditions': ['Angina', 'Heart Attack', 'Anxiety'], 'department': 'Cardiology'},
    'back pain': {'possible_conditions': ['Muscle Strain', 'Herniated Disc', 'Sciatica'], 'department': 'Orthopedics'},
    'stomach pain': {'possible_conditions': ['Gastritis', 'Food Poisoning', 'Appendicitis', 'IBS'], 'department': 'Gastroenterology'},
    'cough': {'possible_conditions': ['Common Cold', 'Bronchitis', 'Pneumonia', 'Allergies'], 'department': 'General Medicine'},
    'skin rash': {'possible_conditions': ['Allergic Reaction', 'Eczema', 'Psoriasis'], 'department': 'Dermatology'},
    'eye pain': {'possible_conditions': ['Conjunctivitis', 'Eye Strain', 'Glaucoma'], 'department': 'Ophthalmology'},
    'ear pain': {'possible_conditions': ['Ear Infection', 'Wax Buildup'], 'department': 'ENT'},
    'joint pain': {'possible_conditions': ['Arthritis', 'Gout', 'Injury'], 'department': 'Orthopedics'},
    'fatigue': {'possible_conditions': ['Anemia', 'Thyroid Issues', 'Sleep Disorders', 'Depression'], 'department': 'General Medicine'},
    'sore throat': {'possible_conditions': ['Tonsillitis', 'Pharyngitis', 'Common Cold'], 'department': 'ENT'},
}

RULE_BASED_CONDITIONS = {
    'fever,cough,sore throat': {'condition': 'Upper Respiratory Infection', 'department': 'General Medicine', 'urgency': 'non-urgent'},
    'fever,cough,shortness of breath': {'condition': 'Possible Pneumonia', 'department': 'General Medicine', 'urgency': 'urgent'},
    'chest pain,shortness of breath,sweating': {'condition': 'Possible Heart Attack', 'department': 'Cardiology', 'urgency': 'emergency'},
    'severe headache,vomiting,sensitivity to light': {'condition': 'Possible Migraine or Meningitis', 'department': 'Neurology', 'urgency': 'urgent'},
    'stomach pain,vomiting,fever': {'condition': 'Possible Gastroenteritis', 'department': 'Gastroenterology', 'urgency': 'non-urgent'},
}


def check_symptoms(symptoms_text):
    symptoms = [s.strip().lower() for s in symptoms_text.split(',')]

    matched_symptoms = []
    for symptom in symptoms:
        for key in SYMPTOM_DATABASE:
            if key in symptom or symptom in key:
                matched_symptoms.append(key)

    matched_symptoms = list(set(matched_symptoms))

    if not matched_symptoms:
        return {
            'possible_conditions': ['Unable to determine. Please consult a doctor.'],
            'department': 'General Medicine',
            'urgency': 'unknown',
            'disclaimer': 'This is not a medical diagnosis. Please consult a healthcare professional.'
        }

    symptoms_key = ','.join(sorted(matched_symptoms))
    rule_match = RULE_BASED_CONDITIONS.get(symptoms_key)

    if rule_match:
        result = rule_match
    else:
        departments = {}
        for s in matched_symptoms:
            if s in SYMPTOM_DATABASE:
                for cond in SYMPTOM_DATABASE[s]['possible_conditions']:
                    departments[cond] = SYMPTOM_DATABASE[s]['department']

        result = {
            'possible_conditions': list(departments.keys()),
            'department': next(iter(departments.values())) if departments else 'General Medicine',
            'urgency': 'non-urgent',
        }

    result['matched_symptoms'] = matched_symptoms
    result['disclaimer'] = 'This is not a medical diagnosis. Please consult a healthcare professional.'
    return result


def check_symptoms_api(symptoms_text):
    api_key = os.getenv('AI_API_KEY', '')
    api_url = os.getenv('AI_API_URL', '')

    if api_key and api_url:
        try:
            import requests
            response = requests.post(
                api_url,
                headers={'Authorization': f'Bearer {api_key}'},
                json={'symptoms': symptoms_text}
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f'AI API call failed: {str(e)}')

    return check_symptoms(symptoms_text)
