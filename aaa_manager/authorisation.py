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

AUTHORISATION_COLLECTION = 'Authorisation'
AUTHORISATION_KEY = 'username'
AUTHORISATION_ITEM = 'resource_rule'

class Authorisation:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.basedb = BaseDB(host, port)

    def verify(self, username, resource):
        """

        """
        return True

    def use_resource(self, username, resource_name):
        """

        """
        if user_exists(username):
            # user resource code
            self.update_resource_item(username,resource_name)

    def validate_rule(self, rule):
        return True

    def user_exists(self, username):
        return True

    def resource_unique(self, resource_name):
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
        if validate_rule(rule)\
        and self.user_exists(username)\
        and self.resource_unique(resource_name):
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



