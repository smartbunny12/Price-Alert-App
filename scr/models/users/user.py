import uuid
from scr.common.database import Database
import scr.models.users.errors as UserErrors
from scr.common.utility import Utils
from scr.models.alerts.alert import Alert
import scr.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an email/password combo(as sent by the site forms) is valid or not
        Check the email exits, and the password associated to the email is corrected
        :param: the user email
        :param: a sha512 hash password
        :return: True if valid, False otherwise
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {'email':email}) # password in sha512 -> pbkdf2_sha512
        if user_data is None:
            # tell user their email doesn't exist
            raise UserErrors.UserNotExistsError('Your user does not exits')

        if not Utils.check_hashed_password(password, user_data['password']):
            # tell user that their password is wrong
            raise UserErrors.IncorrectPasswordError('Your password is wrong')

        return True


    @staticmethod
    def register_user(email, password):
        """
        Register user with email and password;
        The password has already comes hashed as sha512
        :param email: user's email(might be invalid)
        :param password: sha512-hashed
        :return: True if successful, False otherwise(exception can be raised)
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {'email':email})

        if user_data is not None:
            # tell user they have already registered
            raise UserErrors.UserAlreadyRegistedError('The email has already exits')

        if not Utils.email_is_valid(email):
            # tell user that email is not constructed propely
            raise UserErrors.InvalidEmailError('The email does not has the right format')

        User(email, Utils.hash_password(password)).save_to_db()

        return True


    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())


    def json(self):
        return {
            '_id':self._id,
            'email':self.email,
            'password':self.password
        }



    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email':email}))


    def get_alert(self):
        return Alert.find_by_user_email(self.email)