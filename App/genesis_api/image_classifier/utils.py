from genesis_api import db
from genesis_api.config import Config
from werkzeug.utils import secure_filename
from genesis_api.models import User, Image, UserImage

import os

def save_image(user, image_file):
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
                           element="some_element", precision=0.14)

    # Add the new UserImage to the database
    db.session.add(user_image)
    db.session.commit()

    return user_image


def allowed_file(filename: str) -> bool:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
