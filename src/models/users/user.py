import uuid

from src.common.database import Database
import src.models.users.errors as UserErrors
#it will allow us to use the error classes with reference only to User errors
from src.common.utils import Utils
import src.models.users.constants as UserConstants
from src.models.alerts.alert import Alert


class User(object):
    def __init__(self, email, password, user_name, _id=None):
        self.email = email
        self.password = password
        self.user_name = user_name
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User name {}, Email {}>".format(self.user_name, self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        this method verifies that an email/password combo ( as sent by site forms) is valid or not.
        check that the e-mail exists, and that the password associated to that email is correct
        :param email the user's email
        :param password A sha512 hasshed password
        :return True if valid, Flase otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email}) #password in sha512 --> pdkdf2_sha512
        if user_data is None:
            # Tell the user his email does not exist
            raise UserErrors.UserNotExistsError("Your user does not exist")
        # decided not to use the hashed password
        #elif not Utils.check_hashed_password(password, user_data['password']):
        elif password != user_data['password']:
            # Tell the user his password is invalid
            raise UserErrors.IncorrectPasswordError("Wrong password")
        else:
            return  True

    @staticmethod
    def register_user(user_name, email, password):
        """
        This method register a user using e-mail and password.
        the password already comes hashed as sha-512
        :param name: the user name
        :param email: user's e-mail (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise
        (exceptions can also be raised)
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})  # password in sha512 --> pdkdf2_sha512
        if user_data is not None:
            # need to tell the user are already exist
            raise UserErrors.UserAlreadyRegisteredError("The user you tried to register is already exist")
        user_data = Database.find_one(UserConstants.COLLECTION, {"user_name": user_name})
        if user_data is not None:
            # need to tell the user are already exist
            raise UserErrors.UserAlreadyRegisteredError("User with the same name is already exist")
        if not Utils.email_is_valid(email):
            # Tell the user his email is not constructed well
            raise UserErrors.InvalidEmailError("The email you inserted is invalid")
        # Save the user to DB
        user = User(email, password, user_name)
        user.save_to_mongo()

        return True

    def save_to_mongo(self):
        # pass the blog to mongoDb
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        # return json representation of the object
        return {
            'user_name': self.user_name,
            'email': self.email,
            'password': self.password,
            '_id': self._id
        }

    @classmethod
    def get_by_email(cls, email):
        user_data = Database.find_one(UserConstants.COLLECTION, {'email': email})
        if user_data == None:
            return None
        else:
            return cls(**user_data)

    @classmethod
    def get_by_id(cls, _id):
        user_data = Database.find_one(UserConstants.COLLECTION, {'_id': _id})
        if user_data == None:
            return None
        else:
            return cls(**user_data)


    def get_alerts(self):
        return Alert.find_by_user_email(self.email)


