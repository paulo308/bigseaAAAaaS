"""
Email class is responsible for managing favorite information associated to a 
certain user, which will be identified by username.

"""
from aaa_manager.authentication import _DEFAULT_DB_HOST, _DEFAULT_DB_PORT
from aaa_manager.basedb import BaseDB
from jsonschema import validate, ValidationError
import logging


LOG = logging.getLogger(__name__)
FAVORITE_COLLECTION = 'Authorisation'
FAVORITE_KEY = 'username'
FAVORITE_ITEM = 'resource_rule'

class Favorites:

    def __init__(self, host=_DEFAULT_DB_HOST, port=_DEFAULT_DB_PORT):
        self.host = host
        self.port = port
        self.basedb = BaseDB(host, port)

    def create(self, username, favorite_info):
        """
        Create an favorite associated to username on database. 

        Args:
            username (str): username;
            favorite_info (dict): favorite information.

        Returns:
            database response
        """
        if self.validate_favorite(favorite_info):
            item = {
                    'favorite_info': favorite_info,
                    }
            return self.basedb.insert(
                    FAVORITE_COLLECTION,
                    FAVORITE_KEY,
                    username,
                    FAVORITE_ITEM,
                    item)
        return None

    def read(self, username, favorite):
        """
        Read favorite information for username. 

        Args: 
            username (str): username;
            favorite_info (dict): favorite;
            
        """
        result = self.basedb.get(
                FAVORITE_COLLECTION, 
                FAVORITE_KEY,
                username)
        for item in result:
            if item['favorite'] == favorite:
                return item
        return None

    def update(self, username, favorite_info):
        pass

    def delete(self, username, favorite_info):
        pass
    
    def validate_favorite(self, favorite_info):
        SCHEMA = {
                    'type': 'object',
                    'properties': 
                    {
                        'favorite': 
                        {
                            'type': 'string',
                            "pattern": "[^@]+@[^@]+\.[^@]+",
                        },
                    },
                    'required' : ['favorite']
                }
        try:
            validate(favorite_info, SCHEMA)
        except ValidationError as err:
            LOG.error('Invalid favorite')
            raise Exception('Invalid favorite') from err 
        return True
