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

from aaa_manager.basedb import BaseDB
from aaa_manager.accounting import Accounting, INFO
from jsonschema import validate, ValidationError
import json
import logging
import copy

LOG = logging.getLogger(__name__)
AUTHORISATION_COLLECTION = 'Authorisation'
AUTHORISATION_KEY = 'username'
AUTHORISATION_ITEM = 'resource_rule'

class Authorisation:
    """
    Authorisation class is responsible for managing resource usage rules.
    """
    
    def __init__(self):
        self.basedb = BaseDB()
        self.accounting = Accounting()

    def verify(self, username, resource_name, resource_category):
        """
        Returns True if username is allowed to access resource.
        """
        resources = list(self.basedb.get(AUTHORISATION_COLLECTION, 
                AUTHORISATION_KEY,
                username))
        for item in resources:
            for elem in item['resource_rule']:
                LOG.info('elem: %s' % elem)
                if elem['resource_name'] == resource_name and\
                    elem['resource_category'] == resource_category:
                        return True
        return False
    
    def update_resource_item(self, username, resource_name, resource_category):
        """
        Add 1 to used field.
        """
        resources = self.basedb.get(AUTHORISATION_COLLECTION, 
                AUTHORISATION_KEY,
                username)
        for item in resources:
            for elem in item['resource_rule']:
                LOG.info('elem: %s' % elem)
                if elem['resource_name'] == resource_name and\
                        elem['resource_category'] == resource_category:
                    old_item = copy.deepcopy(item)
                    elem['used']= elem['used'] + 1
                    res = self.basedb.update(AUTHORISATION_COLLECTION, 
                            AUTHORISATION_KEY,
                            username, 
                            AUTHORISATION_ITEM,
                            old_item,
                            item)
        return res


    def use_resource(self, username, resource_name, resource_category):
        """
        This method is called in order to user a determined resource. Thus, it
        is responsible for triggering the accounting mechanism and updating the
        database to increment the number of times that resource was used. 
        """
        if self.verify(username, resource_name, resource_category):
            # add 1 to used field
            self.update_resource_item(username, resource_name, resource_category)
            # account it  
            msg = "Resource " + resource_name + " used by: " + username + "."
            LOG.info('msg: %s' % msg)
            category = INFO
            self.accounting.register(username, msg, category)
            return {'msg': msg}
        return None



    def validate_rule(self, rule):
        """
        Validates authorisation object.
        """

        SCHEMA = {
                    'type': 'object',
                    'properties': 
                    {
                        'resource_name': 
                        {
                            'type': 'string',
                            'minLength': 1,
                            'maxLength': 50
                        },
                        'resource_category':
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
                    },
                    'required' : ['resource_category','resource_name', 'max_used']
                }
        try:
            validate(rule, SCHEMA)
        except ValidationError as err:
            LOG.error('Invalid rule')
            raise Exception('Invalid rule') from err 
        return True

    def create(self, username, resource_category, resource_name, max_used):
        """
        Create an authorisation rule on database. 

        Args:
            username (str): username;
            resource_name (str): name that identifies the resource being used;
            rule (dict): rule object.

        Returns:
            database response
        """
        rule = {
                    'resource_category': resource_category,
                    'resource_name': resource_name,
                    'max_used': int(max_used),
                    'used': 0
                }
        if self.validate_rule(rule):
            result = self.basedb.insert(
                    AUTHORISATION_COLLECTION,
                    AUTHORISATION_KEY,
                    username,
                    AUTHORISATION_ITEM,
                    rule)
            if result is not None:
                LOG.info('Rule: ' + json.dumps(rule) + 
                        'successfully created for user: ' + username + 
                        '.')
                return result
        return None

    def read(self, username, resource_name, resource_category):
        """
        Read rule information from user.
        """
        resources = self.basedb.get(
                AUTHORISATION_COLLECTION, 
                AUTHORISATION_KEY,
                username)
        for item in resources:
            for elem in item[AUTHORISATION_ITEM]:
                if elem['resource_name'] == resource_name and\
                        elem['resource_category'] == resource_category:
                    return elem
        return None


    def update(self, username, resource_name, resource_category, max_allowed):
        """
        Update rule information. 
        """
        resources = self.basedb.get(
                AUTHORISATION_COLLECTION, 
                AUTHORISATION_KEY,
                username)
        for item in resources:
            for elem in item[AUTHORISATION_ITEM]:
                if elem['resource_name'] == resource_name and\
                        elem['resource_category'] == resource_category:
                    new_elem = copy.deepcopy(elem)
                    new_elem['max_allowed'] = max_allowed
                    result = self.basedb.update(
                            AUTHORISATION_COLLECTION,
                            AUTHORISATION_KEY,
                            username,
                            AUTHORISATION_ITEM,
                            elem,
                            new_elem)
                    return result
        return None

    def delete(self, username, resource_name, resource_category):
        """
        Delete rule information. 
        """
        resources = self.basedb.get(
                AUTHORISATION_COLLECTION, 
                AUTHORISATION_KEY,
                username)
        for item in resources:
            for elem in item[AUTHORISATION_ITEM]:
                if elem['resource_name'] == resource_name and\
                        elem['resource_category'] == resource_category:
                        result = self.basedb.remove_list_item(
                                AUTHORISATION_COLLECTION,
                                AUTHORISATION_KEY,
                                username,
                                AUTHORISATION_ITEM,
                                elem)
                        return result
        return None

