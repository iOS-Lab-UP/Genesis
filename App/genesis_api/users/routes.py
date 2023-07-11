from flask import Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Assuming you have defined the User and Profile models and initialized the engine
# Create a session factory

from genesis_api.users.utils import *
from genesis_api import db
from genesis_api.tools.utils import parse_request, generate_response
from genesis_api.security import token_required

user = Blueprint('user', __name__)
Session = sessionmaker(bind=db.engine)

@user.route('/sign_up', methods=['POST'])
def sign_up_endpoint() -> dict[str:str]:
    args = parse_request({"name": str, "username": str, "email": str, "password": str, "birth_date": str, "profile_id": int})
    session = Session()

    try:
        user = create_user(session, **args)
        return generate_response(True, 'User was successfully created', user, 200), 200
    except Exception as e:
        return generate_response(False, 'Could not create user', None, 500, str(e)), 500    
    finally:
        session.close()

@token_required
@user.route('/get_user_data', methods=['GET'])
def get_user_data_endpoint() -> dict[str:str]:
    '''Get user information'''
    args = parse_request("id", data_type=int)

    try:
        user = get_user(args['id'])
        return generate_response(True, f'User: {user.id}', user.to_dict(), 200)
    except Exception as e:
        return generate_response(False, 'Could not get user', None, 500, str(e))

@user.route('/updateUser', methods=['PUT'])
def update_user() -> dict[str:str]:
    '''Update user information'''
    args = parse_request("id", "name", "username", "email", "password", "birth_date")
    args['password'] = generate_password_hash(args['password'])

    try:
        user = update_user(**args)
        return generate_response(True, 'User updated', get_user(user.id).to_dict(), 200)
    except Exception as e:
        return generate_response(False, 'Could not update user', None, 400, str(e))

@user.route('/deleteUser', methods=['DELETE'])
def delete_user() -> dict[str:str]:
    '''Delete user'''
    args = parse_request("id", data_type=int)

    try:
        user = delete_user(**args)
        return generate_response(True, f'User: {user.name}', get_user(user.id).to_dict(), 200)
    except Exception as e:
        return generate_response(False, 'Could not delete user', None, 400, str(e))
