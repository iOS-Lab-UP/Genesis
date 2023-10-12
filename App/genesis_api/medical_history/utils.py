from genesis_api import db
from genesis_api.models import User, Profile, VerificationCode, DoctorPatientAssociation, UserImage, Image, MedicalHistory
from genesis_api.tools.handlers import *
from genesis_api.tools.utils import *


def create_medical_history_report(session: any, user_id: int, **kwargs: dict[str,type]) -> dict[str,str]:
    """
    Create a new medical history report for a patient.
    """
    # Get the doctor
    doctor = session.query(User).filter_by(id=user_id).first()
    if not doctor:
        raise InvalidRequestParameters('Doctor not found')
    
    # Get the patient and the doctor-patient association id
    patient = session.query(User).filter_by(id=kwargs['patient_id']).first()
    if not patient:
        raise InvalidRequestParameters('Patient not found')
    association = session.query(DoctorPatientAssociation).filter_by(doctor_id=doctor.id, patient_id=patient.id).first()

    # Get the last image uploaded by doctor
    img = session.query(UserImage).filter_by(user_id=doctor.id).order_by(UserImage.id.desc()).first()

    # Create the medical history report
    medical_history = MedicalHistory(
        doctor_patient_association_id=association.id,
        observation=kwargs['observation'],
        next_appointment=kwargs['next_appointment'], # AAAA-MM-DD
        diagnostic=kwargs['diagnostic'],
        prescription=kwargs['prescription'],
        symptoms=kwargs['symptoms'],
        private_notes=kwargs['private_notes'],
        patient_feedback=kwargs['patient_feedback'],
        follow_up_required=kwargs['follow_up_required'],
    )
    medical_history.user_image = img.id
    session.add(medical_history)
    session.commit()

    # Return the medical history report
    return medical_history.to_dict()





    

    


