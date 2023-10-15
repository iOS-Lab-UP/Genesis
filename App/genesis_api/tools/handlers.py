class UserAlreadyExistsError(Exception):
    """Error raised when user already exists in DB"""

    def __init__(self, message=None):
        self.message: str = "User already exists in the database" if message is None else message


class InvalidRequestParameters(Exception):
    pass

class DuplicateEntryError(Exception):
    """Raised when a duplicate database entry is attempted."""
    pass

class IncorrectCredentialsError(Exception):
    '''Custom exception class for incorrect user credentials'''
    pass


class InvalidUserInput(Exception):
    '''Custom Exception to handle invalid input from users.'''
    pass


class InvalidVerificationCode(Exception):
    '''Custom Exception to handle invalid verificaton codes from user'''
    pass


class RelationshipAlreadyExistsError(Exception):
    '''Custom Exception to handle relationship already existing in DB'''
    pass

class UserNotFoundError(Exception):
    '''Custom Exception to handle user not found in DB'''
    pass

class InternalServerError(Exception):
    '''Custom Exception to handle internal server errors'''
    pass

class ElementNotFoundError(Exception):
    '''Custom Exception to handle element not found in DB'''
    pass