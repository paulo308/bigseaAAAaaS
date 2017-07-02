"""
Email class is responsible for managing email information associated to a 
certain user, which will be identified by username.

"""
from aaa_manager.authentication import _DEFAULT_DB_HOST, _DEFAULT_DB_PORT
from aaa_manager.basedb import BaseDB
from jsonschema import validate, ValidationError
import logging


LOG = logging.getLogger(__name__)
EMAIL_COLLECTION = 'Emails'
EMAIL_KEY = 'username'
EMAIL_ITEM = 'emails'

class Emails:

    def __init__(self, host=_DEFAULT_DB_HOST, port=_DEFAULT_DB_PORT):
        self.host = host
        self.port = port
        self.basedb = BaseDB(host, port)

    def exists(self, email):
        result = self.basedb.get_all(EMAIL_COLLECTION)
        for item in result:
            for elem in item[EMAIL_ITEM]:
                LOG.info('elem: %s' % elem)
                if 'email' in elem:
                    email_item = elem['email']
                    if email_item == email:
                        return False
        return True

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
            if self.exists(email_info['email']):
                return self.basedb.insert(
                        EMAIL_COLLECTION,
                        EMAIL_KEY,
                        username,
                        EMAIL_ITEM,
                        email_info)
        return None
    
    def read_all(self, username):
        """
        Read email information for username. 

        Args: 
            username (str): username;
            
        Returns:
            array of email_info.
        """
        result = self.basedb.get(
                EMAIL_COLLECTION, 
                EMAIL_KEY,
                username)
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
