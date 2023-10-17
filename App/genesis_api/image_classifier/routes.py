from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from genesis_api.tools.handlers import *
from genesis_api.image_classifier.utils import *
from genesis_api.tools.utils import generate_response
from genesis_api.security import *
from genesis_api import db
import re
import json


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

        # print all the elements of the form

        # assuming the ImmutableMultiDict is stored in a variable called data
        diagnostic = request.form.get('diagnostic')
        if diagnostic:
            try:
                # Parse the JSON string to convert it into a Python dictionary
                diagnostic_dict = json.loads(diagnostic)
                print(diagnostic_dict)
            except json.JSONDecodeError:
                return jsonify(success=False, message="Invalid JSON in 'diagnostic' field"), 400

            # Now you can access the values in the dictionary
            for prediction in diagnostic_dict:
                sickness = prediction.get('sickness')
                precision = prediction.get('precision')
                print(f"Sickness: {sickness}, Precision: {precision}")
        else:
            print("No diagnostic data found.")
        # Check if the required arguments are present

        # Perform further validation on element and precision if needed

        # Retrieve the user
        if not current_user:
            return generate_response(False, 'User not found', None, 404), 404

        # Save the image and create a UserImage record
        user_image = save_image(current_user, file)

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

        # Get all UserImage records for this user
        user_images = UserImage.query.filter_by(user_id=current_user.id).all()

        # Extract the image IDs
        image_data = []
        for user_image in user_images:
            image_info = get_image_data(user_image.image_id)
            if image_info is None:
                return generate_response(False, 'Error retrieving image data', None, 500), 500
            image_data.append(image_info.to_dict())

        # Return the image data
        return generate_response(True, 'Image data successfully retrieved', {'images': image_data}, 200)
    except Exception as e:
        return generate_response(False, str(e), None, 500), 500



@image_classifier.route('/get_image/<image_id>', methods=['GET'])
@token_required
def get_image_endpoint(current_user: User, image_id: int) -> dict[str:str]:
    # Retrieve the user
    if not current_user:
        return generate_response(False, 'User not found', None, 404), 404

    # Get the image
    image, error = get_image(current_user, image_id)

    if error:
        return generate_response(False, error, None, 404), 404

    # Return the encoded image
    return generate_response(True, 'Image successfully retrieved', {'image': image}, 200)

@image_classifier.route('/get_user_images_data', methods=['GET'])
@token_required
def get_user_image_endpoint(current_user: User) -> dict[str:str]:
    # Retrieve the user
    if not current_user:
        return generate_response(False, 'User not found', None, 404), 404

    # Get the image
    return generate_response(True, 'Image successfully retrieved', {'image': get_user_image(current_user)
}, 200)

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