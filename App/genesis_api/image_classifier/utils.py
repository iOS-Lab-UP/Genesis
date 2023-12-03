# Standard library imports
import os
import logging

import base64


from typing import Optional
from io import BytesIO
from PIL import Image as PILImage

# Third-party library imports
import base64
import cv2
import numpy as np


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
    user_image = UserImage.query.filter_by(
        user_id=user.id, image_id=image_id).first()

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


def get_user_images_data(current_user: id) -> list[dict[str, str]]:
    # Get all UserImage records for this user
    user_images = UserImage.query.filter_by(user_id=current_user.id).all()

    # Extract the image IDs and apply filters
    image_data = []
    for user_image in user_images:
        image_info = Image.get_data(user_image.image_id).to_dict()
        image_path = os.path.join(Config.UPLOAD_FOLDER, image_info['name'])

        # Encode the image to base64
        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        image_info['image'] = encoded_string

        # Add additional details
        image_info['ml_diagnostic'] = [MlDiagnostic.get_data(
            ml_id.id).to_dict() for ml_id in user_image.ml_diagnostics]

        image_data.append(image_info)

    # Apply filters to the images
    filtered_image_data = apply_filters_to_images(image_data)

    return filtered_image_data


def get_user_image(user: User, image_id: Optional[int] = None) -> list[dict[str, str]]:
    # Get all UserImage records for this user
    user_images = UserImage.query.filter_by(user_id=user.id).all()

    # Extract the image IDs
    image_data = []
    if not image_id:
        for user_image in user_images:
            image_info = Image.get_data(user_image.image_id).to_dict()
            image_path = os.path.join(Config.UPLOAD_FOLDER, image_info['name'])

            # Encode the resized image to base64
            with open(image_path, "rb") as img_file:
                encoded_string = base64.b64encode(
                    img_file.read()).decode('utf-8')
            image_info['image'] = encoded_string

            image_info['ml_diagnostic'] = [MlDiagnostic.get_data(
                ml_id.id).to_dict() for ml_id in user_image.ml_diagnostics]

            image_data.append(image_info['image'], "here")

    else:
        image_info = Image.get_data(image_id).to_dict()
        image_path = os.path.join(Config.UPLOAD_FOLDER, image_info['name'])

        # Resize the image to a maximum size (e.g., 300x300 pixels)

        # Encode the resized image to base64
        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        image_info['image'] = encoded_string

        user_image = db.session.query(UserImage).filter(
            UserImage.image_id == image_id).first()

        image_info['ml_diagnostic'] = [
            MlDiagnostic.get_data(ml_id.id).to_dict() for ml_id in user_image.ml_diagnostics]

        image_data = image_info

    return image_data


def get_doctor_patient_files(doctor_id: int, patient_id: int) -> list[str]:
    """ Get all the images associated with a doctor and a patient """

    # Get all the patients associated with the doctor
    patients = session.query(User).\
        join(DoctorPatientAssociation, DoctorPatientAssociation.patient_id == User.id).\
        filter(DoctorPatientAssociation.doctor_id == doctor_id).\
        all()

    # Get all the images associated with each patient
    images = []
    for patient in patients:
        patient_images = session.query(UserImage).\
            filter(UserImage.user_id == patient.id).\
            all()
        images.extend(patient_images)

    return [image.to_dict() for image in images]


def create_mldiagnostic(sickness, precision, user_image_id) -> MlDiagnostic:
    # Define de ML directory
    try:
        ml_model = MlDiagnostic(
            sickness=sickness, precision=precision, description="description")
        db.session.add(ml_model)
        db.session.commit()

        # Create a new MlDiagnosticImage record
        image = UserImage.get_data(user_image_id)
        image.ml_diagnostics.append(ml_model)

    except SQLAlchemyError as e:
        logging.exception("An error occurred while saving an image: %s", e)
        raise InternalServerError(e)
    return ml_model


def apply_filters_to_images(image_data_list):
    filtered_images = []

    for image_info in image_data_list:
        # Decode the base64 image
        image_bytes = base64.b64decode(image_info['image'])
        image = PILImage.open(BytesIO(image_bytes))
        img = np.array(image.convert('RGB'))

        # Apply filters
        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Extract individual channels
        red_channel = img[:, :, 0]
        green_channel = img[:, :, 1]
        blue_channel = img[:, :, 2]

        # Calculate a mask based on the red channel
        threshold_value = 120
        red_mask = (red_channel > threshold_value) & (
            green_channel < threshold_value) & (blue_channel < threshold_value)

        # Apply the mask to the original image
        img_red_highlighted = np.copy(img_rgb)
        img_red_highlighted[~red_mask] = [0, 0, 0]

        # Convert to grayscale
        gray_img = cv2.cvtColor(img_red_highlighted, cv2.COLOR_RGB2GRAY)

        # Apply Sobel operator to highlight edges
        sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

        # Normalize the magnitude
        magnitude_normalized = np.uint8(255 * magnitude / np.max(magnitude))

        # Convert the filtered image back to PIL Image for encoding
        filtered_image_pil = PILImage.fromarray(magnitude_normalized)

        # Convert the PIL Image to a base64 string
        buffered = BytesIO()
        filtered_image_pil.save(buffered, format="JPEG")
        encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Update the image info with the new filtered image
        image_info_filtered = image_info.copy()
        image_info_filtered['image_filtered'] = encoded_string

        filtered_images.append(image_info_filtered)

    return filtered_images
