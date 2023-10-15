from genesis_api import db
from genesis_api.models import User, Profile, VerificationCode, DoctorPatientAssociation, UserImage, Image
from genesis_api.security import encodeJwtToken, expire_token
from genesis_api.tools.handlers import *
from genesis_api.tools.utils import *
from genesis_api.config import Config


from flask_bcrypt import generate_password_hash
from datetime import datetime
from smtplib import SMTPException
from email.message import EmailMessage

import random
import logging
import requests
import ssl
import smtplib


def create_user(session: any, name: str, username: str, email: str, password: str, birth_date: datetime, profile_id: int, cedula: str = None) -> User:
    '''Create a user and return a User object type'''

    if not is_username_valid(session, username) or not is_valid_email(session, email) or not session.query(Profile).filter(Profile.id == profile_id).first():
        raise InvalidRequestParameters(
            'User already exists in the database. Please try again with a different email or username.')

    if cedula or profile_id == 2:
        if not validate_doctor_identity(cedula, name):
            raise ValueError(
                'You could not be registered as a doctor because your identity could not be validated. Please try again with a different cedula.')

    try:
        user = User(name=name, username=username, email=email, password_hash=generate_password_hash(
            password).decode('utf-8'), birth_date=birth_date, profile_id=profile_id, cedula=cedula, status=0)
        session.add(user)
        session.commit()

        user_data = user.to_dict()
        user_data['jwt_token'] = encodeJwtToken(user_data)
        return user_data

    except Exception as e:
        session.rollback()
        logging.error(e)
        raise


def sign_in(session: any, username: str, password: str) -> User:
    '''Sign in function in order to authenticate user'''

    try:
        user = session.query(User).\
            filter(User.username == username).\
            filter(User.status == 1).\
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
        session.rollback()
        logging.error(e)
        raise


def sign_out(session: any, jwt_token: str) -> User:
    '''Sign out function in order to sign out user by adding jwt token to redis'''
    try:
        Config.REDIS_CLIENT.set(jwt_token, 'expired')
    except Exception as e:
        session.rollback()
        logging.error(e)



def get_user(id: int) -> dict[str:str]:
    '''Get user function in order to get user's info from DB'''

    try:
        return User.get_data(id)
    except Exception as e:
        logging.error(e)
        return None


def validate_user_data(session: any, user_data: User, profile_id: int, cedula: str) -> dict:

    validated_data = {}

    if 'name' in user_data:
        validated_data['name'] = user_data['name']

    if 'username' in user_data:
        validated_data['username'] = user_data['username'] if is_username_valid(
            session, user_data['username']) else None

    if 'email' in user_data:
        validated_data['email'] = user_data['email'] if is_valid_email(
            session, user_data['email']) else None

    if 'password' in user_data:
        validated_data['password_hash'] = generate_password_hash(
            user_data['password']).decode('utf-8')

    if 'birth_date' in user_data:
        validated_data['birth_date'] = user_data['birth_date']

    if profile_id == 2 and not validate_doctor_identity(cedula, user_data['name']):
        raise ValueError(
            'You could not be registered as a doctor because your identity could not be validated. Please try again with a different cedula.'
        )

    return validated_data


def update_user(session: any, current_user_id: int, **user_data: User) -> User:
    '''Update user function in order to update user's info from DB'''

    user = session.query(User).filter(User.id == current_user_id).first()
    if user and user.check_password(user_data.get('password', '')):
        validated_data = validate_user_data(
            session, user_data, user.profile_id, user.cedula)
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


def generate_verification_code(session: any, current_user_id: User) -> str:
    '''Generate verification code in order to generate verification code'''
    try:
        if not session.query(VerificationCode).filter(VerificationCode.user_id == current_user_id).first():
            verificaton_code = VerificationCode(user_id=current_user_id, code=''.join(
                ''.join(random.choice('0123456789') for _ in range(5))))
            db.session.add(verificaton_code)
            db.session.commit()
        else:
            verificaton_code = update_verification_code(
                session, current_user_id)

        return verificaton_code
    except Exception as e:
        session.rollback()
        logging.error(e)
        raise


def update_verification_code(session: any, user_id: User) -> str:
    '''Update verification code associated to user_id in db'''
    try:
        verificaton_code = session.query(VerificationCode).filter(
            VerificationCode.user_id == user_id).first()
        if verificaton_code:
            verificaton_code.code = ''.join(
                random.choice('0123456789') for _ in range(5))
            
            session.commit()
            return verificaton_code

        else:
            raise ValueError(
                f'Verification code for user with id: {user_id} does not exist in the database'
            )

    except Exception as e:
        session.rollback()
        logging.error(e)
        raise


def send_verification_code(user: dict[User], code: str) -> None:
    """Send a verification code to the given email."""
    mail = EmailMessage()
    mail['From'] = Config.MAIL_EMAIL
    mail['To'] = user['email']
    mail['Subject'] = 'Verification Code'
    mail.add_header('Content-Type', 'text/html',)

    html = f'''
    <html>
    <body>
    <h2>Hello {user['name']}!</h2>

    Your verification code is <b>{code}</b>.

    Please enter this code to verify your account.

    </body>
    </html>
    '''
    send_email(mail, html)

def send_email(mail, html):
    mail.set_payload(html)
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP('smtp.gmail.com', Config.MAIL_PORT) as smtp:
            smtp.ehlo()  # Can be omitted
            smtp.starttls(context=context)
            smtp.ehlo()  # Can be omitted
            smtp.login(Config.MAIL_EMAIL, Config.MAIL_PASSWORD)
            smtp.sendmail(mail['From'], mail['To'],
                          mail.as_string().encode('utf-8'))
            smtp.quit()
        
    except smtplib.SMTPException as e:
        logging.error('Error sending email: %s', e)


def verify_code(session: any, user_id: int, code: str) -> User:
    '''Compare the user input code to the one in DB associated to him,
        if they are equal, set user status to 1 else raise an error
    '''
    try:
        verification_code = session.query(VerificationCode).\
            filter(VerificationCode.user_id == user_id).\
            filter(VerificationCode.code == code).first()
        if not verification_code or verification_code.is_expired():
            raise InvalidVerificationCode(
                'Invalid verification code, resend it or input it again'
            )
        else:
            user = session.query(User).filter(User.id == user_id).first()
            user.status = True
            session.add(user)  # Explicitly add changed user instance
            verification_code.expire(session)
            session.flush()  # Add this line to synchronize session's state with DB
            session.commit()  # Ensure this is being called
            return user
    except Exception as e:
        logging.error(e)
        session.rollback()  # Rollback the session in case of error
        raise

def send_doctor_patient_association_email(session: any, doctor_id: int, patient_username: str) -> None:
    """
    Params:
        session: SQLAlchemy session
        doctor_id: int
        patient: it can be either a username
    """

    # Get the doctor's email
    doctor_email = session.query(User).filter_by(id=doctor_id).first().email

    # Get the patient's email
    patient_email = session.query(User).filter_by(username=patient_username).first().email

    # Send the email to the patient
    mail = EmailMessage()
    mail['From'] = Config.MAIL_EMAIL
    mail['To'] = patient_email
    mail['Subject'] = 'Doctor Patient Association'
    mail.add_header('Content-Type', 'text/html',)


    
   




def create_doctor_patient_association(session: any, doctor_id: int, patient_username: int) -> str:
    """ Register an association between a doctor and a patient """
    
    patient_id = session.query(User).filter_by(username=patient_username).first().id

    # Check if an association already exists
    existing_association = session.query(DoctorPatientAssociation).\
        filter_by(doctor_id=doctor_id, patient_id=patient_id).first()
    
    if existing_association:
        raise RelationshipAlreadyExistsError("The relationship already exists")
    
    # Create a new association
    association = DoctorPatientAssociation(doctor_id=doctor_id, patient_id=patient_id)
    session.add(association)
    session.commit()


def get_patients(session: any) -> list[User]:
    """ Get all the patients associated with a doctor """
    try:

        patients = [patient.to_dict() for patient in session.query(User).filter_by(profile_id=1).all()]
        return patients
    except Exception as e:
        logging.error(e)
        session.rollback()
        raise



def get_doctor_patient_files(session: any, doctor_id: int) -> list[str]:
    """ Get all the images associated with a doctor and a patient """

    # Get all the patients associated with the doctor
    patients = session.query(User).\
        join(DoctorPatientAssociation, DoctorPatientAssociation.patient_id == User.id).\
        filter(DoctorPatientAssociation.doctor_id == doctor_id).\
        all()
    
    print(patients)

    # Get all the images associated with each patient
    images = []
    for patient in patients:
        patient_images = session.query(UserImage).\
            filter(UserImage.user_id == patient.id).\
            all()
        images.extend(patient_images)

    return [image.to_dict() for image in images]