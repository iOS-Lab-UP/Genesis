from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from genesis_api.tools.handlers import *
from genesis_api.image_classifier.utils import *
from genesis_api.tools.utils import generate_response
from genesis_api.security import *
from genesis_api import limiter, cache
import re
import json


image_classifier = Blueprint('image_classifier', __name__)


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

        # print all the elements of the form

        # assuming the ImmutableMultiDict is stored in a variable called data
        diagnostic = request.form.get('diagnostic')
        if diagnostic:
            try:
                # Parse the JSON string to convert it into a Python dictionary
                diagnostic_dict = json.loads(diagnostic)
            except json.JSONDecodeError:
                return jsonify(success=False, message="Invalid JSON in 'diagnostic' field"), 400

            # Now you can access the values in the dictionary

        else:
            print("No diagnostic data found.")
        # Check if the required arguments are present

        # Retrieve the user
        if not current_user:
            return generate_response(False, 'User not found', None, 404), 404

        # Save the image and create a UserImage record
        user_image = save_image(current_user, file)
        for prediction in diagnostic_dict:
            create_mldiagnostic(prediction.get('sickness'),
                                prediction.get('precision'), user_image.id)

        return generate_response(True, 'Image successfully uploaded', user_image.to_dict(), 201), 201
    else:
        return generate_response(False, 'File type not allowed', None, 400), 400


@image_classifier.route('/get_user_images', methods=['GET'])
@token_required
def get_user_images_endpoint(current_user: User) -> dict[str:str]:
    try:
        # Retrieve the user
        if not current_user:
            return generate_response(False, 'User not found', None, 404), 404

        # Return the image data
        return generate_response(True, 'Image data successfully retrieved', {'images': get_user_images_data(current_user)}, 200)
    except Exception as e:
        return generate_response(False, str(e), None, 500), 500


@image_classifier.route('/get_image/<image_id>', methods=['GET'])
@token_required
@limiter.limit("15 per minute")
def get_user_image_by_id_endpoint(current_user: User, image_id: int) -> dict[str:str]:
    # Retrieve the user
    if not current_user:
        return generate_response(False, 'User not found', None, 404), 404
    return generate_response(True, 'Image successfully retrieved', get_user_image(current_user, image_id), 200)


@image_classifier.route('/get_user_images_data', methods=['GET'])
@token_required
@limiter.limit("15 per minute")
def get_user_image_endpoint(current_user: User) -> dict[str:str]:
    # Retrieve the user
    if not current_user:
        return generate_response(False, 'User not found', None, 404), 404
    return generate_response(True, 'Image successfully retrieved', {'images': get_user_images_data(current_user)}, 200)


@image_classifier.route('/get_doctor_patient_files/<patient_id>', methods=['GET'])
@token_required
def get_doctor_patient_files_endpoint(current_user: User, patient_id) -> dict[str:str]:
    try:
        files = get_doctor_patient_files(current_user.id, patient_id)
        return generate_response(True, 'Files retrieved', files, 200), 200
    except Exception as e:
        return generate_response(False, 'Could not get files', None, 500, str(e)), 500
    finally:
        session.close()
