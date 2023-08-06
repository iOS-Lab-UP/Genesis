from genesis_api import db
from genesis_api.config import Config
from werkzeug.utils import secure_filename
from genesis_api.models import User, Image, UserImage

import base64
from flask import send_from_directory

import os
import logging

def save_image(user, image_file, element, precision):
    # Define the image directory
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
    user_image = UserImage(user_id=user.id, image_id=new_image.id,
                           element=element, precision=precision)

    # Add the new UserImage to the database
    db.session.add(user_image)
    db.session.commit()

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
        print(id)
        return Image.get_data(id)
    except Exception as e:
        logging.error(e)
        return None