from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from genesis_api.medical_history.utils import *
from genesis_api.tools.handlers import *
from genesis_api.tools.utils import parse_request, generate_response
from genesis_api.image_classifier.utils import *
from genesis_api.security import *
from genesis_api import db, limiter, cache

medical_history = Blueprint(
    'medical_history', __name__, url_prefix='/medical_history')
Session = sessionmaker(bind=db.engine)


@medical_history.route('/new_report', methods=['POST'])
@token_required
@limiter.limit("30 per minute")  # Apply rate limiting
def post_medical_history_endpoint(current_user: User) -> dict[str:str]:
    fields = {"observation": str, "next_appointment": str, "diagnostic": str,  "symptoms": str,
              "private_notes": str, "follow_up_required": bool, "patient_id": int, "user_image": int, "prescription": list}
    required_fields = ["next_appointment", "diagnostic",  "symptoms",
                       "follow_up_required", "patient_id", "user_image"]

    try:
        args = parse_request(fields, 'json', required_fields)
        medical_history = create_medical_history_report(
            current_user.id, **args)
        return generate_response(True, 'Medical History was successfully created', medical_history, 201), 201
    except InvalidRequestParameters as e:
        return generate_response(False, 'Invalid request parameters', None, 400, str(e)), 400
    except Exception as e:
        return generate_response(False, 'Could not create Medical History', None, 500, str(e)), 500


@medical_history.route('get_medical_history/<int:patient_id>', methods=['GET'])
@token_required
@limiter.limit("30 per minute")  # Apply rate limiting
@cache.cached(timeout=300, key_prefix='medical_history')
def get_medical_history_endpoint(current_user: User, patient_id: int) -> dict[str:str]:

    try:
        # Assuming there's a function to retrieve medical history in utils
        medical_history = get_medical_history_by_patient(
            current_user, patient_id)
        if medical_history:
            return generate_response(True, 'Medical History retrieved successfully', medical_history, 200), 200
        else:
            return generate_response(False, 'Medical History not found', None, 404), 404
    except Exception as e:
        return generate_response(False, 'Could not retrieve Medical History', None, 500, str(e)), 500


@medical_history.route('get_my_medical_history', methods=['GET'])
@token_required
@limiter.limit("30 per minute")  # Apply rate limiting
@cache.cached(timeout=300, key_prefix='medical_history')
def get_my_medical_history_endpoint(current_user: User) -> dict[str:str]:

    try:
        # Assuming there's a function to retrieve medical history in utils
        medical_history = get_my_medical_history(current_user)
        if medical_history:
            return generate_response(True, 'Medical History retrieved successfully', medical_history, 200), 200
        else:
            return generate_response(False, 'Medical History not found', None, 404), 404
    except Exception as e:
        return generate_response(False, 'Could not retrieve Medical History', None, 500, str(e)), 500


@medical_history.route('/send_patient_feedback', methods=['PATCH'])
@token_required
@limiter.limit("5 per minute")  # Apply rate limiting
def send_patient_feedback_endpoint(current_user: User) -> dict[str:str]:
    fields = {"feedback": str, "medical_history_id": int}
    required_fields = ["feedback", "medical_history_id"]

    try:
        args = parse_request(fields, 'json', required_fields)
        send_patient_feedback(current_user.id, **args)
        return generate_response(True, 'Patient feedback was successfully sent', None, 200), 200
    except InvalidRequestParameters as e:
        return generate_response(False, 'Invalid request parameters', None, 400, str(e)), 400
    except Exception as e:
        return generate_response(False, 'Could not send patient feedback', None, 500, str(e)), 500
