
from flask import Blueprint
from genesis_api.tools.handlers import *
from genesis_api.users.utils import *
from genesis_api.tools.utils import parse_request, generate_response
from genesis_api.security import *
from genesis_api import db, limiter, cache


user = Blueprint('user', __name__)
executor = ThreadPoolExecutor(2)


@user.route('/sign_up', methods=['POST'])
@limiter.limit("5 per minute")  # Apply rate limiting
@sql_injection_free
def sign_up_endpoint() -> dict[str:str]:

    fields = {"name": str, "username": str, "email": str, "password": str,
              "birth_date": str, "profile_id": int, "cedula": str}
    required_fields = ["name", "username", "email",
                       "password", "birth_date", "profile_id"]

    try:
        args = parse_request(fields, 'json', required_fields)
        user = create_user(**args)
        if user:
            verification_code = generate_verification_code(user['id'])
            send_verification_code(executor, user, verification_code.code)

        return generate_response(True, 'User was successfully created', user, 201), 201
    except InvalidRequestParameters as e:
        return generate_response(False, 'Invalid request parameters', None, 400, str(e)), 400
    except Exception as e:
        return generate_response(False, 'Could not create user', None, 500, str(e)), 500


@user.route('/sign_up/verify_identity', methods=['POST'])
@token_required
@sql_injection_free
def verify_identity_endpoint(current_user: User) -> dict[str:str]:
    fields = {"code": str}
    required_fields = ["code"]

    try:
        args = parse_request(fields, 'json', required_fields)
        user = verify_code(current_user.id, **args)
        return generate_response(True, 'User was successfully verified', user.to_dict(), 201), 201
    except InvalidRequestParameters as e:
        return generate_response(False, 'Invalid request parameters', None, 400, str(e)), 400
    except InvalidVerificationCode as e:
        return generate_response(False, 'Invalid verification code', None, 401, str(e)), 401
    except Exception as e:
        return generate_response(False, 'Could not verify user', None, 500, str(e)), 500


@user.route('/sign_up/resend_verification_code', methods=['GET'])
@token_required
def resend_verification_code_endpoint(current_user: User) -> dict[str:str]:

    try:
        verification_code = generate_verification_code(current_user.id)
        send_verification_code(
            executor, current_user.to_dict(), verification_code.code)
        return generate_response(True, 'Verification code was successfully sent', None, 200), 200
    except Exception as e:
        return generate_response(False, 'Could not send verification code', None, 500, str(e)), 500


@user.route('/sign_in', methods=['POST'])
@sql_injection_free
def sign_in_endpoint() -> dict[str:str]:
    try:
        args = parse_request({"username": str, "password": str})
        user = sign_in(**args)
        return generate_response(True, 'User was successfully authenticated', user, 200), 200
    except InvalidRequestParameters as e:
        return generate_response(False, 'Invalid request parameters', None, 400, str(e)), 400
    except IncorrectCredentialsError as e:
        return generate_response(False, 'Incorrect credentials', None, 401, str(e)), 401
    except Exception as e:
        return generate_response(False, 'Could not authenticate user', None, 500, str(e)), 500


# TODO: Implement this endpoint
@user.route('/sign_out', methods=['GET'])
@token_required
def sign_out_endpoint(current_user: User) -> tuple[dict[str, any], int]:
    '''Sign out user'''
    try:
        sign_out(request.headers['x-access-token'])
        return generate_response(True, 'User was successfully signed out', None, 200), 200
    except Exception as e:
        return generate_response(False, 'Could not sign out user', None, 500, str(e)), 500


@user.route('/get_user_data', methods=['GET'])
@token_required
def get_user_data_endpoint(current_user: User) -> tuple[dict[str, any], int]:
    '''Get user information'''
    try:
        username = request.args.get('username')
        if username:
            user = User.query.filter_by(username=username).first()
        else:
            user = get_user(id=current_user.id)

        if user:
            return generate_response(True, f'User: {user.id}', user.to_dict(), 200), 200
        else:
            return generate_response(False, 'User not found', None, 404), 404
    except Exception as e:
        return generate_response(False, 'Could not get user', None, 500, str(e)), 500


@user.route('/update_user_data', methods=['PUT'])
@token_required
@sql_injection_free
def update_user_endpoint(current_user: User) -> dict[str:str]:
    '''Update user information'''
    fields = {"name": str, "username": str,
              "email": str, "password": str, "birth_date": str}
    args = parse_request(fields)
    if len(args) == 0:
        return generate_response(False, 'No fields to update', None, 400), 400

    try:
        user = update_user(current_user.id, **args)
        return generate_response(True, 'User data updated', get_user(user.id).to_dict(), 200), 200
    except Exception as e:
        return generate_response(False, 'Could not update user', None, 500, str(e)), 500

# TODO: Need to finish this endpoint


@user.route('/deleteUser', methods=['DELETE'])
@sql_injection_free
def delete_user() -> dict[str:str]:
    '''Delete user'''
    args = parse_request("id", data_type=int)

    try:
        user = delete_user(**args)
        return generate_response(True, f'User: {user.name}', get_user(user.id).to_dict(), 200)
    except Exception as e:
        return generate_response(False, 'Could not delete user', None, 400, str(e))

# TODO: Create endpoint to change user's password


@user.route('/get_patients', methods=['GET'])
@token_required
def get_patients_endpoint() -> dict[str:str]:
    try:
        patients = get_users_by_profile(1)
        return generate_response(True, 'Patients retrieved', patients, 200), 200
    except Exception as e:
        return generate_response(False, 'Could not get patients', None, 500, str(e)), 500


@user.route('/get_user_to_user_relation', methods=['GET'])
@token_required
def get_patient_doctors_endpoint(user_id: int) -> dict[str:str]:
    try:
        users = get_user_to_user_relation(user_id.id)
        return generate_response(True, 'Users retrieved', users, 200), 200
    except Exception as e:
        return generate_response(False, 'Could not get doctors', None, 500, str(e)), 500


@user.route('/create_doctor_patient_association', methods=['POST'])
@token_required
@sql_injection_free
def create_doctor_patient_association_endpoint(current_user: User) -> dict[str:str]:
    fields = {"patient_username": str}
    required_fields = ["patient_username"]

    try:
        args = parse_request(fields, 'json', required_fields)
        association = create_doctor_patient_association(
            current_user.id, **args)
        return generate_response(True, 'Association created', association, 201), 201
    except InvalidRequestParameters as e:
        return generate_response(False, 'Invalid request parameters', None, 400, str(e)), 400
    except Exception as e:
        return generate_response(False, 'Could not create association', None, 500, str(e)), 500


@user.route('/new_password', methods=['PATCH'])
@token_required
@limiter.limit("5 per minute")  # Apply rate limiting
@sql_injection_free
def new_password_endpoint(current_user: User) -> dict[str:str]:
    fields = {"current_password": str, "new_password": str}
    required_fields = ["current_password", "new_password"]
    try:
        args = parse_request(fields, 'json', required_fields)
        new_password(current_user.id, **args)
        return generate_response(True, 'Password was successfully changed', None, 200), 200
    except InvalidRequestParameters as e:
        return generate_response(False, 'Invalid request parameters', None, 400, str(e)), 400
    except Exception as e:
        return generate_response(False, 'Could not change password', None, 500, str(e)), 500


@user.route('/get_users', methods=['GET'])
@token_required
def get_users_endpoint(current_user: User) -> dict[str:str]:
    try:
        users = get_users()
        return generate_response(True, 'Users retrieved', users, 200), 200
    except Exception as e:
        return generate_response(False, 'Could not get users', None, 500, str(e)), 500
