from genesis_api.models import User
from genesis_api.tools.handlers import InvalidRequestParameters
from flask import session, jsonify
from contextlib import contextmanager
from datetime import datetime
from genesis_api import db
from flask_restful import reqparse
from werkzeug.exceptions import BadRequest
from email_validator import validate_email, EmailNotValidError

import psutil


def server_status() -> str:
    '''
    Check if the server is up and running
    OK: memory usage < 80% and cpu usage < 80%
    SLOW: memory usage < 80% and cpu usage > 80%
    CRITICAL: memory usage > 80% and cpu usage > 80%
    '''
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    status = ""
    if memory.percent < 80 and cpu < 80:
        status = "OK"
    elif memory.percent < 80 and cpu > 80:
        status = "SLOW"
    else:
        status = "CRITICAL"
    return status


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def color(color: int, text: str) -> str:
    '''
    1: Red
    2: Green
    3: Yellow
    4: Blue
    5: Purple
    6: Cyan
    '''

    match color:
        case 1:
            return f"\033[1;31;40m{text}\033[0m"
        case 2:
            return f"\033[1;32;40m{text}\033[0m"
        case 3:
            return f"\033[1;33;40m{text}\033[0m"
        case 4:
            return f"\033[1;34;40m{text}\033[0m"
        case 5:
            return f"\033[1;35;40m{text}\033[0m"
        case 6:
            return f"\033[1;36;40m{text}\033[0m"
        case _:
            raise ValueError("Invalid color")


def deleteUserSession() -> None:
    '''Deletes the user session'''
    session.pop('user', None)
    session.pop('logged_in', None)


def writeHTMLFile(rows: list) -> None:
    with open('App/school/dashboard/upsite.html', 'w') as f:
        f.write("<!DOCTYPE html>\n<html>\n<body>\n")
        source_codes = [row.get_attribute('innerHTML') for row in rows]
        f.write('\n'.join(source_codes))
        f.write("\n</body>\n</html>")


def parse_request(args_types: dict, location='json', required_args=None):
    parser = reqparse.RequestParser(bundle_errors=True)
    for arg, data_type in args_types.items():
        required = arg in required_args if required_args else False
        parser.add_argument(arg, type=data_type,
                            location=location, required=required)
    try:
        args = parser.parse_args(strict=True)
        # Remove any keys with value None
        args = {key: value for key, value in args.items() if value is not None}
        return args
    except BadRequest as e:
        # Handle missing or incorrect arguments
        raise InvalidRequestParameters(
            f"Missing arguments or incorrect data types")



def generate_response(success: bool, message: str, data: dict, status: int, error: str = None) -> dict:
    response = {
        'success': success,
        'message': message,
        'status': status,
    }
    if error is not None:
        response['error'] = error
    if data is not None:
        response['data'] = data
    return response


def split_names(nombre: str) -> list[str]:
    tokens = nombre.split(" ")
    names = []
    special_tokens = ['da', 'de', 'di', 'do', 'del', 'la', 'las',
                      'le', 'los', 'mac', 'mc', 'van', 'von', 'y', 'i', 'san', 'santa']
    previous = ""

    for token in tokens:
        lowercase_token = token.lower()

        if lowercase_token in special_tokens:
            previous += token + " "
        else:
            names.append(previous + token)
            previous = ""

    num_names = len(names)
    first_name, last_name1, last_name2 = "", "", ""

    if num_names == 0:
        first_name = ""
    elif num_names == 1:
        first_name = names[0]
    elif num_names == 2:
        first_name = names[0]
        last_name1 = names[1]
    elif num_names == 3:
        first_name = names[0]
        last_name1 = names[1]
        last_name2 = names[2]
    else:
        first_name = names[0] + " " + names[1]
        last_name1 = names[2]
        last_name2 = names[3]

    first_name = first_name.title()
    last_name1 = last_name1.title()
    last_name2 = last_name2.title()

    name_lastname = [first_name, (last_name1 + ' ' + last_name2)]
    return name_lastname


def is_valid_email(session: any, email_address: str) -> bool:
    '''Check if the email address is valid and not already in the database'''
    try:
        # Check that the email address is valid
        emailinfo = validate_email(email_address, check_deliverability=False)

        # After this point, use only the normalized form of the email address,
        # especially before going to a database query.
        email_address = emailinfo.normalized

        # Check if the email exists in the database
        email_exists = session.query(User).filter(
            User.email == email_address).first() is not None

        return not email_exists

    except EmailNotValidError:
        return False


def is_username_valid(session, username):
    """Check if username is valid."""
    # Check if username is lowercase
    if not username.islower():
        return False

    # Check if username exists in the database
    if session.query(User).filter(User.username == username).first():
        return False

    return True
