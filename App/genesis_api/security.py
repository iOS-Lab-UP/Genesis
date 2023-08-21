from datetime import datetime, timedelta
from functools import wraps
from typing import Callable
from flask import request, jsonify


from genesis_api.tools.utils import color
from genesis_api import Config
from genesis_api.models import User
from genesis_api.tools.handlers import *

import logging
import jwt
import traceback

def token_required(func):
    '''Decorator to check if the user has a valid token'''
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # Decode the token to get user data
            data = jwt.decode(token,
                              Config.SECRET_KEY,
                              algorithms=['HS256'])
            
            # Check if the token has expired
            current_time = datetime.utcnow()
            print( current_time)
            if 'exp' in data and data['exp'] < current_time:
                return jsonify({'message': 'Token has expired!'}), 401
            
            # Get the user associated with the decoded data (assumed to be a user ID)
            current_user = User.query.filter_by(id=data['public_id']).first()
            if not current_user:
                return jsonify({'message': 'User not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.DecodeError:
            return jsonify({'message': 'Token is invalid!'}), 401

        # Call the decorated function with the current_user argument
        return func(current_user, *args, **kwargs)

    return decorator




def encodeJwtToken(user: dict[str, str]) -> dict[str, str]:
    '''Encodes a user object into a JWT token'''
    try:
        if user:
            token = jwt.encode({
                'public_id': user['id'],
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'username': user['username'],
                    'email': user['email'],
                    'profile_id': user['profile_id'],
                    'exp': str(datetime.utcnow() + timedelta(days=50))
                }
            },
                Config.SECRET_KEY,
                algorithm='HS256')
        else:
            raise ValueError(f'{color(3,"User object is empty")}')
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt encode token")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        token = None

    return token

def get_jwt_identity():
    '''Extracts the public_id (user_id) from the JWT token in the current request.'''
    token = None
    # Check if token is in the headers
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']

    # If no token is found, return None
    if not token:
        raise IncorrectCredentialsError('Token is missing!')

    try:
        # Decode the token to get user data
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        # Return the public_id from the decoded data
        return data['public_id']
    except Exception as e:
        print(e)
        return None

def expire_token(user_id: int) -> None:
    '''Expires a user's token by modifying the date'''
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.token_expiration = datetime.utcnow()
        user.save()
    else:
        raise UserNotFoundError('User not found!')

def sql_injection_free(func):
    """Decorator to check if incoming JSON data is free from SQL injection attempts."""
    @wraps(func)
    def decorator(*args, **kwargs):
        data = request.get_json()
        for value in data.values():
            if not is_sql_injection_free(str(value)):
                return jsonify({'message': 'Invalid input'}), 400
        return func(*args, **kwargs)
    return decorator


def is_sql_injection_free(input_string):
    """Check if input_string is free from SQL injection attempts."""
    # Convert the input to lower case
    input_lower = input_string.lower()

    # List of SQL keywords that might be used in an injection attack
    keywords = ['select', 'insert', 'update',
                'delete', 'drop', '--', '/*', '*/', 'xp_', ';']

    # Check if any keyword is in the input
    if any(keyword in input_lower for keyword in keywords):
        return False
    else:
        return True
