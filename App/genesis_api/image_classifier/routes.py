from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from genesis_api.tools.handlers import *
from genesis_api.image_classifier.utils import *
from genesis_api.tools.utils import generate_response
from genesis_api.security import *
from genesis_api import db

image_classifier = Blueprint('image_classifier', __name__)
Session = sessionmaker(bind=db.engine)


@image_classifier.route('/upload_image', methods=['POST'])
@token_required
def upload_image_endpoint(current_user: User) -> dict[str:str]:
    # Check if the post request has the file part
    if 'file' not in request.files:
        return generate_response(False, 'No file part', None, 400), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return generate_response(False, 'No selected file', None, 400), 400

    if file and allowed_file(file.filename):
        # Get other required arguments
        element = request.form.get('element')
        precision = request.form.get('precision')

        # Check if the required arguments are present
        if not element or not precision:
            return generate_response(False, 'Missing required arguments', None, 400), 400

        # Perform further validation on element and precision if needed

        # Retrieve the user
        if not current_user:
            return generate_response(False, 'User not found', None, 404), 404

        # Save the image and create a UserImage record
        user_image = save_image(current_user, file, element, precision)

        return generate_response(True, 'Image successfully uploaded', user_image.to_dict(), 201), 201
    else:
        return generate_response(False, 'File type not allowed', None, 400), 400
