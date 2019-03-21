import re
#adding regular expression lib

from passlib.hash import pbkdf2_sha512

class Utils(object):
    @staticmethod
    def hash_password(password):
        """
        hashes a password using pdkdf2_sha512
        :param password: the sha512 password from login/register forms
        :return: a sha512-->pdkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        check that password of user sent mathces that of the database
        the database password is encrypted more thn the user password at this stage
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        """
        check if email is valid by regualr expretion
        :param email: the inserted email to validate
        :return: True is the email is matching the regular expression, else False
        """
        #define new matcher based on the regaulr expression
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False