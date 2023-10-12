from flask import Blueprint
from sqlalchemy.orm import sessionmaker

from genesis_api.medical_history.utils import *
from genesis_api.tools.handlers import *
from genesis_api.tools.utils import parse_request, generate_response
from genesis_api.image_classifier.utils import *
from genesis_api.security import *
from genesis_api import db, limiter, cache

medical_history = Blueprint('medical_history', __name__, url_prefix='/medical_history')
Session = sessionmaker(bind=db.engine)



@medical_history.route('/new_status', methods=['POST'])
@token_required
@limiter.limit("5 per minute")  # Apply rate limiting
def get_medical_history(current_user: User) -> dict[str:str]:
    session = Session()
    fields = {"observation":str, "next_appointment":str, "diagnostic":str, "prescription":str, "symptoms":str,
              "private_notes":str, "patient_feedback":str, "follow_up_required":bool, "patient_id":int, "user_image":int}
    required_fields = ["next_appointment", "diagnostic", "prescription", "symptoms",
                       "private_notes", "patient_feedback", "follow_up_required", "patient_id", "user_image"]
    
    try:
        args = parse_request(fields, 'json', required_fields)
        medical_history = create_medical_history_report(session, current_user.id,**args)
        return generate_response(True, 'Medical History was successfully created', medical_history, 201), 201
    except InvalidRequestParameters as e:
        return generate_response(False, 'Invalid request parameters', None, 400, str(e)), 400
    except Exception as e:
        return generate_response(False, 'Could not create Medical History', None, 500, str(e)), 500
    finally:
        session.close()


@medical_history.route('/', methods=['POST'])
def create_medical_history():
    pass

@medical_history.route('/<int:id>', methods=['PUT'])
def update_medical_history(id):
    pass

@medical_history.route('/<int:id>', methods=['DELETE'])
def delete_medical_history(id):
    pass
