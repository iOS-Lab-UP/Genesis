from genesis_api import db
from genesis_api.models import User, Profile
from genesis_api.security import encodeJwtToken

from flask_bcrypt import generate_password_hash
from datetime import datetime
from sqlalchemy.orm import close_all_sessions

import logging


def create_user(session: any, name: str, username: str, email: str, password: str, birth_date: datetime, profile_id: int) -> User:
    '''Create a user and return a User object type'''

    try:
        if not session.query(User).filter_by(email=email).first() and not session.query(User).filter_by(username=username).first() and session.query(Profile).filter_by(id=profile_id).first():
            user = User(name=name, username=username, email=email,
                        password_hash=generate_password_hash(password).decode('utf-8'), birth_date=birth_date, profile_id=profile_id)
            session.add(user)
            session.commit()

            user_data = user.to_dict()
            user_data['jwt_token'] = encodeJwtToken(user_data)
            return user_data
        else:
            raise ValueError(
                f'User already exists in the database. Please try again with a different email or username.'
            )
    except Exception as e:
        session.rollback()
        logging.error(e)
        raise
    finally:
        close_all_sessions()  # Close all open sessions


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
