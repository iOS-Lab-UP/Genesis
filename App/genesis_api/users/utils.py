from genesis_api import db
from genesis_api.models import User, Profile
from genesis_api.security import encodeJwtToken
from genesis_api.tools.handlers import IncorrectCredentialsError
from genesis_api.tools.utils import split_names

from flask_bcrypt import generate_password_hash
from datetime import datetime
from sqlalchemy.orm import close_all_sessions


import logging
import requests

def create_user(session: any, name: str, username: str, email: str, password: str, birth_date: datetime, profile_id: int, cedula: str = None) -> User:
    '''Create a user and return a User object type'''

    if session.query(User).filter(User.email == email).first() or session.query(User).filter(User.username == username).first() or not session.query(Profile).filter(Profile.id == profile_id).first():
        raise ValueError('User already exists in the database. Please try again with a different email or username.')

    if cedula:
        if not validate_doctor_identity(cedula, name):
            raise ValueError('You could not be registered as a doctor because your identity could not be validated. Please try again with a different cedula.')

    try:
        user = User(name=name, username=username, email=email, password_hash=generate_password_hash(password).decode('utf-8'), birth_date=birth_date, profile_id=profile_id, cedula=cedula)
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


def update_user(id: int, name: str, username: str, email: str, password: str, birth_date: datetime) -> User:
    '''Update user function in order to update user's info from DB'''

    try:
        user = User.query.filter_by(id=id).first()
        if user:
            user.name = name
            user.username = username
            user.email = email
            user.password = generate_password_hash(password).decode('utf-8')
            user.birth_date = birth_date
            db.session.commit()
            return user
        else:
            raise ValueError(
                f'User with id: {id} does not exist in the database'
            )

    except Exception as e:
        logging.error(e)
        return None


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