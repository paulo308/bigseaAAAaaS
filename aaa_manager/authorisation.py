"""
Authorisation class is responsible for managing information about which
resources each user is allowed to access. 
Each user is uniquely identified by its username. Thus, it is possible to 
bind username to a set of allowed resources. In order to generalize how each 
resource is described, we are going to use a json object to contain a 
description of that device. This description will have also information about 
how many times that resource was used by that user. It will be possible to 
verify if the number of times the resource was used reached the maximum number
of times this resource is allowed to be used. 
"""

from aaa_manager.authentication import _DEFAULT_DB_HOST, _DEFAULT_DB_PORT
from aaa_manager.basedb import BaseDB
from jsonschema import validate, ValidationError
import logging

LOG = logging.getLogger(__name__)
AUTHORISATION_COLLECTION = 'Authorisation'
AUTHORISATION_KEY = 'username'
AUTHORISATION_ITEM = 'resource_rule'

class Authorisation:
    
    def __init__(self, host=_DEFAULT_DB_HOST, port=_DEFAULT_DB_PORT):
        self.host = host
        self.port = port
        self.basedb = BaseDB(host, port)

    def verify(self, username, resource):
        """

        """
        return True
    
    def update_resource_item(self, username, resource_name):
        return None


    def use_resource(self, username, resource_name):
        """

        """
        if user_exists(username):
            # user resource code
            self.update_resource_item(username, resource_name)

    def validate_rule(self, rule):
        SCHEMA = {'type': 'object',
                'properties': {
                    'resource_name': 
                    {
                        'type': 'string',
                        'minLength': 1,
                        'maxLength': 50
                    },
                    'resource_type':
                    {
                        'type': 'string',
                        'minLength': 1,
                        'maxLength': 50
                    },
                    'max_used':
                    {
                        'type': 'number'
                    },
                    'used':
                    {
                        'type': 'number'
                    },
                    'app_id':
                    {
                        'type': 'number'
                    },
                    'url':
                    {
                        'type': 'string',
                        'minLength': 1,
                        'maxLength': 50
                    },
                    'blob':
                    {
                        'type': 'string',
                        'minLength': 1,
                        'maxLength': 50
                    },
                    },
                    'required' : ['app_id', 'resource_type','resource_name']
                }
        try:
            validate(rule, SCHEMA)
        except ValidationError as err:
            LOG.error('Invalid rule')
            raise Exception('Invalid rule') from err 
        return True

    def create(self, username, resource_name, rule):
        """
        Create an authorisation rule on database. 

        Args:
            username (str): username;
            resource_name (str): name that identifies the resource being used;
            rule (dict): rule object.

        Returns:
            database response
        """
        if self.validate_rule(rule):
            item = {
                    'resource_name': resource_name,
                    'rule': rule
                    }
            return self.basedb.insert(
                    AUTHORISATION_COLLECTION,
                    AUTHORISATION_KEY,
                    username,
                    AUTHORISATION_ITEM,
                    item)
        return None

    def read(self, username, resource_name):
        """

        """
        resources = self.basedb.get(
                AUTHORISATION_COLLECTION, 
                AUTHORISATION_KEY,
                username)
        for item in resources:
            if item['resource_name'] == resource_name:
                return item
        return None


    def update(self):
        pass

    def delete(self):
        pass



