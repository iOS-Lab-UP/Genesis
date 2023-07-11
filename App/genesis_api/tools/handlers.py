class UserAlreadyExistsError(Exception):
    """Error raised when user already exists in DB"""

    def __init__(self, message=None):
        self.message: str = "User already exists in the database" if message is None else message


class InvalidRequestParameters(Exception):
    pass


class IncorrectCredentialsError(Exception):
    '''Custom exception class for incorrect user credentials'''
    pass


class InvalidUserInput(Exception):
    '''Custom Exception to handle invalid input from users.'''
    pass
