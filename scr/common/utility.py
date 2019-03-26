from passlib.hash import pbkdf2_sha512
import re

class Utils(object):


    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False


    @staticmethod
    def hash_password(password):
        """
        Hash a password using pbkdf2_sha512
        :param: sha512 password from login/register form
        :return: a sha512 ->pbfkd2 sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)


    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Check the password that the user sent match with the database password
        The database password is encrypted more than the user's password at this stage
        :param: sha512 password
        :param: pbkdf2_sha512 encrypted password
        :return: True if password match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)