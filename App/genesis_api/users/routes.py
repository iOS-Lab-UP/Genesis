from flask import Blueprint
from genesis_api.users.utils import *
from genesis_api.tools.utils import parse_request, generate_response

user = Blueprint('user', __name__)


@user.route('/sign_up', methods=['POST'])
def sign_up_endpoint() -> dict[str:str]:
    args = parse_request("name", "username", "email", "password", "birth_date", "profile_id")

    try:
        user = create_user(**args)
        return generate_response(True, 'User was successfully created', user, 200)
    except Exception as e:
        return generate_response(False, 'Could not create user', None, 500, str(e))


@user.route('/getUser', methods=['GET'])
def get_user_endpoint() -> dict[str:str]:
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
