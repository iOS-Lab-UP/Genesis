from genesis_api.models import User,  DoctorPatientAssociation, UserImage,  MedicalHistory, Prescription
from genesis_api.tools.handlers import *
from genesis_api.tools.utils import *

from sqlalchemy.orm import Session,joinedload, contains_eager
from sqlalchemy.exc import SQLAlchemyError

import logging


def create_medical_history_report(user_id: int, **kwargs: dict[str,type]) -> dict[str,str]:
    """
    Create a new medical history report for a patient.
    """

    try:
        # Get the patient and the doctor-patient association id
        patient_id = User.get_data(kwargs['patient_id']).id
        if not patient_id:
            raise ElementNotFoundError('Patient not found')
        
        association = db.session.query(DoctorPatientAssociation).filter_by(doctor_id=user_id, patient_id=patient_id).first()
        if not association:
            raise ElementNotFoundError('Doctor-Patient association not found')
        elif db.session.query(MedicalHistory).filter(MedicalHistory.association_id == association.id, MedicalHistory.next_appointment_date==kwargs['next_appointment']).first():
            raise DuplicateEntryError('Medical history report already exists for this patient')
        
        # Create the medical history report
        medical_history = MedicalHistory(
            association_id=association.id,
            observation=kwargs['observation'],
            next_appointment_date=kwargs['next_appointment'], # AAAA-MM-DD
            diagnostic=kwargs['diagnostic'],
            symptoms=kwargs['symptoms'],
            private_notes=kwargs['private_notes'],
            follow_up_required=kwargs['follow_up_required'],
        )
        medical_history.user_images.append(UserImage.get_data(kwargs['user_image']))
        db.session.add(medical_history)
        db.session.commit()
    except Exception as e:
        logging.exception("An error occurred while creating a medical history report: %s", e)
        raise InternalServerError(e)
    except SQLAlchemyError as e:
        logging.exception("An error occurred while creating a medical history report: %s", e)
        raise InternalServerError(e)
        
    # Return the medical history report as a dictionary
    return medical_history.to_dict()



def create_prescription(session: Session, **kwargs:dict[str,type]) -> dict[str,str]:
    """
    Create a new prescription obj
    """

    prescription = Prescription(
        treatment=kwargs['treatment'],
        dosage=kwargs['dosage'],
        frequency=kwargs['frequency'],
        frequency_unit=kwargs['frequency_unit'],
        duration=kwargs['duration'],
        duration_unit=kwargs['duration_unit'],
        medical_history_id=kwargs['medical_history_id']
    )
    session.add(prescription)
    session.commit()

    return prescription.to_dict()






def get_medical_history_by_patient(session: Session, current_user: User, patient_id: int) -> dict:
    """
    Retrieve a patient's medical history from the database.

    :param session: The SQLAlchemy session to use for database interactions.
    :param patient_id: The ID of the patient whose medical history is being retrieved.
    :param current_user: The current user (doctor) making the request.
    :return: A dictionary containing the medical history data, or None if no record was found.
    """
    try:
        # Combine queries to retrieve medical history records directly through the association
        medical_history_records = session.query(MedicalHistory)\
            .join(DoctorPatientAssociation, DoctorPatientAssociation.id == MedicalHistory.association_id)\
            .filter(
                DoctorPatientAssociation.doctor_id == current_user.id,
                DoctorPatientAssociation.patient_id == patient_id
            )\
            .options(
                contains_eager(MedicalHistory.association).joinedload(DoctorPatientAssociation.patient),
                joinedload(MedicalHistory.user_images)  # Eager load user images
            )\
            .all()

        if medical_history_records:
            medical_history_data = []
            for record in medical_history_records:
                record_dict = record.to_dict()
                if record.user_images:  # Only add if there are user images
                    record_dict['user_images'] = [image.to_dict() for image in record.user_images]
                medical_history_data.append(record_dict)

            return medical_history_data
        else:
            return None

    except Exception as e:
        logging.exception("An error occurred while retrieving medical history: %s", e)
        return None


