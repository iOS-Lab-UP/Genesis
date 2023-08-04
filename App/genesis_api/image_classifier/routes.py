from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from genesis_api.tools.handlers import *
from genesis_api.image_classifier.utils import *
from genesis_api.tools.utils import parse_request, generate_response
from genesis_api.security import *
from genesis_api import db

image_classifier = Blueprint('image_classifier', __name__)
Session = sessionmaker(bind=db.engine)


@image_classifier.route('/upload_image', methods=['POST'])
@token_required
@sql_injection_free
def upload_image_endpoint():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return generate_response(False, 'No file part', None, 400), 400
    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return generate_response(False, 'No selected file', None, 400), 400

    if file and allowed_file(file.filename):
        # Retrieve the user
        user = User.query.get(request.form['user_id'])
        if not user:
            return generate_response(False, 'User not found', None, 404), 404

        # Save the image and create a UserImage record
        user_image = save_image(user, file)

        return generate_response(True, 'Image successfully uploaded', user_image.to_dict(), 201), 201
    else:
        return generate_response(False, 'File type not allowed', None, 400), 400