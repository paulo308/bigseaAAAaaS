"""
Email class is responsible for managing email information associated to a 
certain user, which will be identified by username.

"""
from aaa_manager.authentication import _DEFAULT_DB_HOST, _DEFAULT_DB_PORT
from aaa_manager.basedb import BaseDB
from jsonschema import validate, ValidationError
import logging


LOG = logging.getLogger(__name__)
EMAIL_COLLECTION = 'Authorisation'
EMAIL_KEY = 'username'
EMAIL_ITEM = 'resource_rule'

class Emails:

    def __init__(self, host=_DEFAULT_DB_HOST, port=_DEFAULT_DB_PORT):
        self.host = host
        self.port = port
        self.basedb = BaseDB(host, port)

    def create(self, username, email_info):
        """
        Create an email associated to username on database. 

        Args:
            username (str): username;
            email_info (dict): name that identifies the resource being used.

        Returns:
            database response
        """
        if self.validate_email(email_info):
            item = {
                    'email_info': email_info,
                    }
            return self.basedb.insert(
                    EMAIL_COLLECTION,
                    EMAIL_KEY,
                    username,
                    EMAIL_ITEM,
                    item)
        return None

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

    def update(self, username, email_info):
        pass

    def delete(self, username, email_info):
        pass
    
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
