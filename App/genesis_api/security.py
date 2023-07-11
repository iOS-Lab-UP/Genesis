from datetime import datetime, timedelta
from functools import wraps
from typing import Callable
from flask import request, jsonify

from genesis_api.tools.utils import color
from genesis_api import Config
from genesis_api.models import User

import logging
import jwt
import traceback


def token_required(func) -> Callable:
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
            # Get the user associated with the decoded data (assumed to be a user ID)
            current_user = User.get_data(data['public_id'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 404
        except:
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
