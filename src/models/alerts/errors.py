class AlertError(Exception):
    def __init__(self, message):
        self.message = message


# inherit from User Error exception but on top include message
class AlertNotActiveError(AlertError):
    pass