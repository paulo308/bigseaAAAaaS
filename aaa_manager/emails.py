"""
Email class is responsible for managing email information associated to a 
certain user, which will be identified by username.

"""
import logging
from aaa_manager.basedb import BaseDB
from aaa_manager.email_token import EmailToken
from jsonschema import validate, ValidationError


USER_COLLECTION = 'users'
APP_KEY = 'app_id'
USER_ITEM = 'auth'
EMAIL_COLLECTION = 'Emails'
EMAIL_KEY = 'username'
EMAIL_ITEM = 'emails'

LOG = logging.getLogger(__name__)

class Emails:

    def __init__(self):
        self.basedb = BaseDB()
        self.emailToken = EmailToken()

    def create(self, username, email_info):
        """
        Create an email associated to username on database. 

        Args:
            username (str): username;
            email_info (dict): email information.

        Returns:
            database response
        """
        if self.validate_email(email_info):
            if self.is_email_unique(email_info['email']):
                self.emailToken.send_email_token(username, email_info['email'])
                return self.basedb.insert(
                        EMAIL_COLLECTION,
                        EMAIL_KEY,
                        username,
                        EMAIL_ITEM,
                        email_info)
        return None
    
    def is_unique(self, username, email):
        """
        Verifies that the email is unique for the user.
        """
        result = self.basedb.get(EMAIL_COLLECTION, EMAIL_KEY, username)
        for item in result:
            LOG.info('item: %s' % item)
            for elem in item['emails']:
                LOG.info('elem: %s' % elem)
                if elem['email'] == email:
                    return False
        return True
    
    def is_email_unique(self, email):
        """
        Verifies that the email is unique for the app.
        """
        users = self.basedb.get(USER_COLLECTION, APP_KEY, 2)
        for user in users:
            for user_info in user[USER_ITEM]:
                if email == user_info['email']:
                    return False
                if self.is_unique(user_info['username'], email) == False:
                    return False
        return True

    def read_all(self, username):
        """
        Read email information for username. 

        Args: 
            username (str): username;
            
        Returns:
            array of email_info.
        """
        res = self.basedb.get(
                EMAIL_COLLECTION, 
                EMAIL_KEY,
                username)
        result = list(res)
        for item in result:
            del item['_id']
        return result

    def read(self, username, email):
        """
        Read email information for username. 

        Args: 
            username (str): username;
            email_info (dict): email;
            
        """
        result = self.basedb.get(
                EMAIL_COLLECTION, 
                EMAIL_KEY,
                username)
        for item in result:
            if item['email'] == email:
                return item
        return None

    def delete(self, username, email):
        """
        Delete email information for that username.
        """
        result = self.basedb.get(
                EMAIL_COLLECTION, 
                EMAIL_KEY,
                username)
        for item in result:
            for elem in item['emails']:
                if elem['email'] == email:
                    result = self.basedb.remove_list_item(
                            EMAIL_COLLECTION,
                            EMAIL_KEY,
                            username,
                            EMAIL_ITEM,
                            elem)
                    return result
        return None
    
    def validate_email(self, email_info):
        SCHEMA = {
                    'type': 'object',
                    'properties': 
                    {
                        'email': 
                        {
                            'type': 'string',
                            "pattern": "[^@]+@[^@]+\.[^@]+",
                        },
                    },
                    'required' : ['email']
                }
        try:
            validate(email_info, SCHEMA)
        except ValidationError as err:
            LOG.error('Invalid email')
            raise Exception('Invalid email') from err 
        return True
