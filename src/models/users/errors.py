
class UserError(Exception):
    def __init__(self, message):
        self.message = message


# inherit from User Error exception but on top include message
class UserNotExistsError(UserError):
    pass


class IncorrectPasswordError(UserError):
    pass


class UserAlreadyRegisteredError(UserError):
    pass


class InvalidEmailError(UserError):
    pass