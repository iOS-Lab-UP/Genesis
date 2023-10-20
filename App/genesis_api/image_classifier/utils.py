# Standard library imports
import os
import logging
from typing import Optional

# Third-party library imports
import base64
from flask import send_from_directory
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename

# Local imports
from genesis_api import db
from genesis_api.config import Config
from genesis_api.models import *
from genesis_api.tools.utils import *
from genesis_api.tools.handlers import *




def save_image(user, image_file):
    # Define the image directory
    try:
        image_directory = Config.UPLOAD_FOLDER

        # Save the image to the directory
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(image_directory, filename)
        image_file.save(image_path)

        # Create a new Image record
        new_image = Image(path=image_path, name=filename)

        # Add the new image to the database
        db.session.add(new_image)
        db.session.commit()

        # Create a new UserImage record
        user_image = UserImage(user_id=user.id, image_id=new_image.id)

        # Add the new UserImage to the database
        db.session.add(user_image)
        db.session.commit()
    except SQLAlchemyError as e:
        logging.exception("An error occurred while saving an image: %s", e)
        raise InternalServerError(e)

    return user_image


def allowed_file(filename: str) -> bool:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image(user: User, image_id: int):
    # Retrieve the UserImage record
    user_image = UserImage.query.filter_by(user_id=user.id, image_id=image_id).first()

    if not user_image:
        return None, 'Image not found'

    # Retrieve the Image record
    image = Image.query.get(user_image.image_id)

    

    if not image:
        return None, 'Image not found'

    # Encode the image to base64
    with open(os.path.join(Config.UPLOAD_FOLDER, image.name), "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

    return encoded_string, None


def get_image_data(id: int) -> dict[str:str]:
    # Retrieve the Image record

    try:
        
        return Image.get_data(id)
    except Exception as e:
        logging.error(e)
        return None
    
def get_user_image(user: User, image_id: Optional[int] = None) -> list[dict[str, str]]:
    # Get all UserImage records for this user
    user_images = UserImage.query.filter_by(user_id=user.id).all()

    # Extract the image IDs
    image_data = []
    if not image_id:
        for user_image in user_images:
            image_info = Image.get_data(user_image.image_id).to_dict()
            image_path = os.path.join(Config.UPLOAD_FOLDER, image_info['name'])

            # Resize the image to a maximum size (e.g., 300x300 pixels)
            max_size = (300, 300)
            resize_image(image_path, max_size)

            # Encode the resized image to base64
            with open(image_path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
            image_info['image'] = encoded_string

            if image_info is None:
                return None
            image_data.append(image_info)
    else:
        image_info = Image.get_data(image_id).to_dict()
        image_path = os.path.join(Config.UPLOAD_FOLDER, image_info['name'])

        # Resize the image to a maximum size (e.g., 300x300 pixels)
        max_size = (300, 300)
        resize_image(image_path, max_size)

        # Encode the resized image to base64
        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        image_info['image'] = encoded_string

        image_data = image_info

    return image_data

def get_doctor_patient_files(doctor_id: int, patient_id:int) -> list[str]:
    """ Get all the images associated with a doctor and a patient """

    # Get all the patients associated with the doctor
    patients = session.query(User).\
        join(DoctorPatientAssociation, DoctorPatientAssociation.patient_id == User.id).\
        filter(DoctorPatientAssociation.doctor_id == doctor_id).\
        all()
    
    print(patients)

    # Get all the images associated with each patient
    images = []
    for patient in patients:
        patient_images = session.query(UserImage).\
            filter(UserImage.user_id == patient.id).\
            all()
        images.extend(patient_images)

    return [image.to_dict() for image in images]

def create_mldiagnostic(**kwargs) -> MlDiagnostic:
    #Define de ML directory
    try :
        ml_model = MlDiagnostic(**kwargs)
        db.session.add(ml_model) 
        db.session.commit()
    except SQLAlchemyError as e:
        logging.exception("An error occurred while saving an image: %s", e)
        raise InternalServerError(e)
    return ml_model