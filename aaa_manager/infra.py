"""
Infra class is responsible for managing infra credentials.

"""
import logging
from aaa_manager.basedb import BaseDB
from jsonschema import validate, ValidationError


INFRA_COLLECTION = 'Infra'
INFRA_KEY = 'username'
INFRA_ITEM = 'data'

LOG = logging.getLogger(__name__)

class Infra:

    def __init__(self):
        self.basedb = BaseDB()

    def create(self, username, infra_info):
        """
        Create an infra associated to username on database. 

        Args:
            username (str): username;
            infra_info (dict): infra information.

        Returns:
            database response
        """
        result = read(username)
        if result is not None:
            if self.validate_infra(infra_info):
                return self.basedb.insert(
                        INFRA_COLLECTION,
                        INFRA_KEY,
                        username,
                        INFRA_ITEM,
                        infra_info)
        else:
            return None, "alerady has infra data"

        return None
    

    def read(self, username):
        """
        Read infra information for username. 

        Args: 
            username (str): username;
            
        """
        result = self.basedb.get(
                INFRA_COLLECTION, 
                INFRA_KEY,
                username)
        res = list(result)
        for item in res:
            del item['_id']
        return res

    def delete(self, username):
        """
        Delete infra information for that username.
        """
        result = self.basedb.remove(
                INFRA_COLLECTION,
                INFRA_KEY,
                username)
        return result
    
    def validate_infra(self, infra_info):
        SCHEMA = {
                    'type': 'object',
                    'properties': 
                    {
                        'principal': 
                        {
                            'type': 'string',
                            'minLength': 1,
                            'maxLength': 50
                        },
                        'secret': 
                        {
                            'type': 'string',
                            'minLength': 1,
                            'maxLength': 50
                        },
                    },
                    'required' : ['principal', 'secret']
                }
        try:
            validate(infra_info, SCHEMA)
        except ValidationError as err:
            LOG.error('Invalid infra')
            raise Exception('Invalid infra') from err 
        return True
