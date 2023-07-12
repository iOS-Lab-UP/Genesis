from flask import Blueprint
from sqlalchemy.orm import sessionmaker
from genesis_api.tools.handlers import InvalidRequestParameters, IncorrectCredentialsError


from genesis_api.users.utils import *
from genesis_api.tools.utils import parse_request, generate_response
from genesis_api.security import token_required, sql_injection_free
from genesis_api import db

user = Blueprint('user', __name__)
Session = sessionmaker(bind=db.engine)


@user.route('/sign_up', methods=['POST'])
@sql_injection_free
def sign_up_endpoint() -> dict[str:str]:
    session = Session()
    fields = {"name": str, "username": str, "email": str, "password": str,
              "birth_date": str, "profile_id": int, "cedula": str}
    required_fields = ["name", "username", "email",
                       "password", "birth_date", "profile_id"]

    try:
        args = parse_request(fields, 'json', required_fields)
        user = create_user(session, **args)
        return generate_response(True, 'User was successfully created', user, 201), 201
    except InvalidRequestParameters as e:
        return generate_response(False, 'Invalid request parameters', None, 400, str(e)), 400
    except Exception as e:
        return generate_response(False, 'Could not create user', None, 500, str(e)), 500
    finally:
        session.close()


@user.route('/sign_in', methods=['POST'])
def sign_in_endpoint() -> dict[str:str]:
    session = Session()
    try:
        args = parse_request({"username": str, "password": str})
        user = sign_in(session, **args)
        return generate_response(True, 'User was successfully authenticated', user, 200), 200
    except InvalidRequestParameters as e:
        return generate_response(False, 'Invalid request parameters', None, 400, str(e)), 400
    except IncorrectCredentialsError as e:
        return generate_response(False, 'Incorrect credentials', None, 401, str(e)), 401
    except Exception as e:
        return generate_response(False, 'Could not authenticate user', None, 500, str(e)), 500
    finally:
        session.close()


@user.route('/sign_out', methods=['POST'])
@token_required
def sign_out_endpoint(current_user: User) -> tuple[dict[str, any], int]:
    '''Sign out user'''
    session = Session()
    try:
        sign_out(session, current_user.id)
        return generate_response(True, 'User was successfully signed out', None, 200), 200
    except Exception as e:
        return generate_response(False, 'Could not sign out user', None, 500, str(e)), 500


@user.route('/get_user_data', methods=['GET'])
@token_required
def get_user_data_endpoint(current_user: User) -> tuple[dict[str, any], int]:
    '''Get user information'''
    try:
        # Retrieve user data using the authenticated user's ID
        user = get_user(current_user.id)
        return generate_response(True, f'User: {user.id}', user.to_dict(), 200), 200
    except Exception as e:
        return generate_response(False, 'Could not get user', None, 500, str(e)), 500


@user.route('/update_user_data', methods=['PUT'])
@token_required
def update_user_endpoint(current_user: User) -> dict[str:str]:
    '''Update user information'''
    session = Session()
    fields = {"name": str, "username": str, "email": str, "password": str, "birth_date": str}
    args = parse_request(fields)
    if len(args) == 0:
        return generate_response(False, 'No fields to update', None, 400), 400

    try:
        user = update_user(session, current_user.id, **args)
        return generate_response(True, 'User data updated', get_user(user.id).to_dict(), 200), 200
    except Exception as e:
        return generate_response(False, 'Could not update user', None, 500, str(e)), 500


@user.route('/deleteUser', methods=['DELETE'])
def delete_user() -> dict[str:str]:
    '''Delete user'''
    args = parse_request("id", data_type=int)

    try:
        user = delete_user(**args)
        return generate_response(True, f'User: {user.name}', get_user(user.id).to_dict(), 200)
    except Exception as e:
        return generate_response(False, 'Could not delete user', None, 400, str(e))
