
class StoreError(Exception):
    def __init__(self, message):
        self.message = message


# inherit from User Error exception but on top include message
class StoreNotFoundError(StoreError):
    pass