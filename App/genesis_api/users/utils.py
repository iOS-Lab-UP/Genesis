from genesis_api import db
from genesis_api.models import User, Profile
from genesis_api.security import encodeJwtToken
from genesis_api.tools.handlers import IncorrectCredentialsError, InvalidRequestParameters
from genesis_api.tools.utils import *

from flask_bcrypt import generate_password_hash
from datetime import datetime
from sqlalchemy.orm import close_all_sessions


import logging
import requests


def create_user(session: any, name: str, username: str, email: str, password: str, birth_date: datetime, profile_id: int, cedula: str = None) -> User:
    '''Create a user and return a User object type'''

    if not is_username_valid(session, username) or not is_valid_email(session, email) or not session.query(Profile).filter(Profile.id == profile_id).first():
        raise InvalidRequestParameters(
            'User already exists in the database. Please try again with a different email or username.')

    if cedula:
        if not validate_doctor_identity(cedula, name):
            raise ValueError(
                'You could not be registered as a doctor because your identity could not be validated. Please try again with a different cedula.')

    try:
        user = User(name=name, username=username, email=email, password_hash=generate_password_hash(
            password).decode('utf-8'), birth_date=birth_date, profile_id=profile_id, cedula=cedula)
        session.add(user)
        session.commit()

        user_data = user.to_dict()
        user_data['jwt_token'] = encodeJwtToken(user_data)
        return user_data

    except Exception as e:
        session.rollback()
        logging.error(e)
        raise

    finally:
        close_all_sessions()  # Close all open sessions


def sign_in(session: any, username: str, password: str) -> User:
    '''Sign in function in order to authenticate user'''

    try:
        user = session.query(User).\
            filter(User.username == username).\
            first()

        if user and user.check_password(password):
            user_data = user.to_dict()
            user_data['jwt_token'] = encodeJwtToken(user_data)
            return user_data
        else:
            raise IncorrectCredentialsError(
                'The provided username or password is incorrect. Please try again.'
            )
    except Exception as e:
        logging.error(e)
        raise
    finally:
        close_all_sessions()


def sign_out(session: any, user_id: int) -> User:
    '''Sign out function in order to sign out user'''
    # TODO: expire the jwt token
    pass


def get_user(id: int) -> dict[str:str]:
    '''Get user function in order to get user's info from DB'''

    try:
        return User.get_data(id)
    except Exception as e:
        logging.error(e)
        return None

def validate_user_data(session:any, user_data: User, profile_id: int, cedula: str) -> dict:
    
    print(user_data)
    validated_data = {}

    if 'name' in user_data:
        validated_data['name'] = user_data['name']

    if 'username' in user_data:
        validated_data['username'] = user_data['username'] if is_username_valid(session, user_data['username']) else None

    if 'email' in user_data:
        validated_data['email'] = user_data['email'] if is_valid_email(session, user_data['email']) else None

    if 'password' in user_data:
        validated_data['password_hash'] = generate_password_hash(user_data['password']).decode('utf-8')

    if 'birth_date' in user_data:
        validated_data['birth_date'] = user_data['birth_date']

    if profile_id == 2 and not validate_doctor_identity(cedula, user_data['name']):
        raise ValueError(
            'You could not be registered as a doctor because your identity could not be validated. Please try again with a different cedula.'
        )

    return validated_data


def update_user(session:any,current_user_id: int, **user_data: User) -> User:
    '''Update user function in order to update user's info from DB'''
    
    user = session.query(User).filter(User.id == current_user_id).first()
    if user and user.check_password(user_data.get('password', '')):
        validated_data = validate_user_data(session, user_data, user.profile_id, user.cedula)
        for field, value in validated_data.items():
            if value is not None:
                setattr(user, field, value)
        
        session.commit()
        return user

    else:
        raise ValueError(
            f'Invalid credentials for user with id: {current_user_id}'
        )



def delete_user(id: int) -> User:
    '''Delete user function in order to delete user's info from DB'''

    try:
        user = User.query.filter_by(id=id).first()
        if user:
            user.status = False
            db.session.commit()
            return user
        else:
            raise ValueError(
                f'User with id: {id} does not exist in the database'
            )

    except Exception as e:
        logging.error(e)
        return None


def validate_doctor_identity(cedula: str, name: str) -> bool:
    '''Validate doctor identity in order to validate doctor's identity'''

    url = "https://www.cedulaprofesional.sep.gob.mx/cedula/buscaCedulaJson.action"

    complete_names = [name_part.upper() for name_part in split_names(name)]
    first_name = complete_names[0]
    last_name_parts = complete_names[1].split(' ')
    last_name1 = last_name_parts[0]
    last_name2 = last_name_parts[1]
    id_cedula = cedula

    # Build the payload string with variables
    payload = f'json=%7B%22maxResult%22%3A%221000%22%2C%22nombre%22%3A%22{first_name}%22%2C%22paterno%22%3A%22{last_name1}%22%2C%22materno%22%3A%22{last_name2}%22%2C%22idCedula%22%3A%22{id_cedula}%22%7D'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    response = requests.post(url, headers=headers, data=payload)

    def is_valid(json, first_name, last_name1, last_name2, id_cedula) -> bool:
        credentials = json['items'][0]
        return (
            credentials['nombre'] == first_name and
            credentials['paterno'] == last_name1 and
            credentials['materno'] == last_name2 and
            credentials['idCedula'] == id_cedula
        )

    return is_valid(response.json(), first_name, last_name1, last_name2, id_cedula)
