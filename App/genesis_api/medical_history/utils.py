from genesis_api import db
from genesis_api.models import User, Profile, VerificationCode, DoctorPatientAssociation, UserImage, Image, MedicalHistory
from genesis_api.tools.handlers import *
from sqlalchemy.orm import Session,joinedload, class_mapper

from genesis_api.tools.utils import *
import logging


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
    # instead of d

    # Create the medical history report
    medical_history = MedicalHistory(
        association_id=association.id,
        observation=kwargs['observation'],
        next_appointment_date=kwargs['next_appointment'], # AAAA-MM-DD
        diagnostic=kwargs['diagnostic'],
        prescription=kwargs['prescription'],
        symptoms=kwargs['symptoms'],
        private_notes=kwargs['private_notes'],
        patient_feedback=kwargs['patient_feedback'],
        follow_up_required=kwargs['follow_up_required'],
    )
    medical_history.user_images.append(session.query(UserImage).get(kwargs['user_image']))
    
    session.add(medical_history)
    session.commit()

    # Return the medical history report
    return medical_history.to_dict()





from sqlalchemy.orm import joinedload

def get_medical_history_by_patient(session: Session, current_user: User, patient_id: int) -> dict:
    """
    Retrieve a patient's medical history from the database.

    :param session: The SQLAlchemy session to use for database interactions.
    :param patient_id: The ID of the patient whose medical history is being retrieved.
    :param current_user: The current user (doctor) making the request.
    :return: A dictionary containing the medical history data, or None if no record was found.
    """
    try:
        # Find the association record for the current doctor and patient
        association = session.query(DoctorPatientAssociation).filter(
            DoctorPatientAssociation.doctor_id == current_user.id,
            DoctorPatientAssociation.patient_id == patient_id
        ).first()

        if association:
            # Query the database to get the medical history record for the specified association
            # and load the user_images relationship
            medical_history_records = session.query(MedicalHistory).filter(
                MedicalHistory.association_id == association.id
            ).options(joinedload(MedicalHistory.user_images)).all()

            if medical_history_records:
                # Convert the SQLAlchemy object(s) to a dictionary
                medical_history_data = []
                for record in medical_history_records:
                    record_dict = record.to_dict()
                    # Add user_images only if there are related records
                    if record.user_images:
                        record_dict['user_images'] = [image.to_dict() for image in record.user_images]
                    medical_history_data.append(record_dict)

                return medical_history_data
            else:
                return None
        else:
            return None

    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred while retrieving medical history: {e}")
        return None


