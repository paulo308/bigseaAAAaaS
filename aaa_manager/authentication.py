"""
An interface to manage users data on database.
It provides methods to insert, update and delete users.
It also support token management. 
"""
import logging
import hashlib
import copy
import json
import datetime
from jsonschema import validate
from enum import Enum
from aaa_manager.basedb import BaseDB

LOG = logging.getLogger(__name__)
_DEFAULT_DB_HOST = 'mongo'
_DEFAULT_DB_PORT = 27017

USER_COLLECTION = 'users'
APP_KEY = 'app_id'
USER_ITEM = 'auth'


class Auth(Enum):
    """ 
    Enumeration used in order to distinguish types of users.
    """
    ADMIN = 1
    USERS = 2

class AuthenticationManager:
    """
    Provides an interface to access and manipulate user data collections.
    It is responsible for implementing authentication business logic. 
    All users belongs to some specific application, which is identified by
    the utilization of `app_id` parameter.
    """

    def __init__(self, host=_DEFAULT_DB_HOST, port=_DEFAULT_DB_PORT):
        self.host = host
        self.port = port
        self.basedb = BaseDB(host, port)

    def _format_user_dict(self, user):
        return {
            APP_KEY: user[APP_KEY],
            USER_ITEM: user[USER_ITEM][0]
        }

    def _is_admin_unique(self, app_id, username):
        """
        Verify if the admin username on app data is unique.

        Args:
            app_id (int): the app key;
            username (str): the username being tested.

        Returns:
            boolean: False if the admin username is already present, True
                otherwise.
        """
        users = list(self.basedb.get(USER_COLLECTION, APP_KEY, app_id))
        for elem in users:
            for elem_item in elem[USER_ITEM]:
                if elem_item['admin']['username'] == username:
                    return False
        return True


    def _is_user_unique(self, app_id, username):
        """
        Verify if the username on a app data is unique.

        Args:
            app_id (int): the app key;
            username (str): the username being tested.

        Returns:
            boolean: False if the user username is already present, True
                otherwise.
        """
        users = list(self.basedb.get(USER_COLLECTION, APP_KEY, app_id))
        for user in users:
            for elem in user[USER_ITEM]:
                if elem['username'] == username:
                    return False
        return True

    def _hash(self, data):
        """
        Compute the hash of a string using SHA-512.

        Args:
            password (str): the password to be hashed.

        Returns:
            str: the digest of the hashed password in hexadecimal digits.
        """
        return hashlib.sha512(data.encode()).hexdigest()

    def get_all_users(self):
        """
        Get all users.

        Returns:
            dict: all users data.
        """
        users = []
        for user in self.basedb.get_all(USER_COLLECTION):
            users.append(self._format_user_dict(user))
        return users

    def delete_user(self, app_id, user_info):
        """
        Delete a user entry on users collection in database.

        Args:
            app_id (int): the app id;
            username (dict): the user information.

        Returns:
            object: The inserted object or None on failure;
            str: 'admin' if the cause of failure was repeated admin 
            authentication, 'users' for a non unique username, 'id' if the
            app_id already exists, 'username' for duplicated username on the 
            auth_info.
        """
        auth = copy.deepcopy(user_info)
        auth['password'] = self._hash(auth['password'])
        return self.basedb.remove_list_item(USER_COLLECTION, APP_KEY, app_id,
                                        USER_ITEM, auth)

    def insert_user(self, app_id, user_info):
        """
        Insert a new user entry on users collection in database.

        Args:
            app_id (int): the app id;
            auth_info (dict): the user dict, should contain users and admin's 
            information and credentials.

        
        Returns:
            object: the inserted object or None if error;
            str: 'admin' for repeated admin authentication, or 'users' for 
            repeated username.
        """
        if user_info['username'] == 'admin':
            return None, 'admin'
        auth = copy.deepcopy(user_info)
        auth['password'] = self._hash(auth['password'])
        if not self._is_user_unique(app_id, auth['username']):
            return None, 'users'

        return self.basedb.insert(USER_COLLECTION, APP_KEY, app_id,
                                        USER_ITEM, auth), ''

    def remove_app(self, app_id):
        """
        Remove an item from users collection in database.

        Args:
            app_id (int): application id.

        Returns:
            object: result of remove operation. 
        """
        return self.basedb.remove(USER_COLLECTION, APP_KEY, app_id)


    def generate_token(self, user):
        """
        Generate a token that can be used to authenticate user to access app. 

        Args:
            user (dict): user information.

        Returns: 
            str: hexadecimal representation of token.
        """
        return self._hash(json.dumps(user)+datetime.datetime.now().
                strftime("%Y-%m-%d %H:%M:%S"))
    
    def remove_token(self, token):
        """
        Remove token from DB.

        Args:
            token (str): hexidecimal token

        Returns: 
            obj: mongodb result
        """
        return self.basedb.remove('Token', 'token', token)

    def insert_token(self, app_id, user, token):
        """Insert token into DB.

        Args:
            app_id (int): application id
            user (dict): user information
            token (str): hexidecimal token

        Returns: 
            obj: mongodb result
        """
        self.basedb.update('Token', 'token', token, 'data', 
                {'app_id': app_id, 'user': user, 'status': 'valid'}, 
                {'app_id': app_id, 'user': user, 'status': 'invalid'})
        return self.basedb.insert('Token', 'token', token, 'data', 
                {'app_id': app_id, 'user': user, 'status': 'valid'})

    def verify_token(self, app_id, token):
        """Verify token validity.

        Args:
            app_id (int): application id
            token (str): hexidecimal token

        Returns:
            str: username corresponding to token if valid, 
            'invalid token' otherwise
        """
        result = list(self.basedb.get('Token', 'token', token))
        for item in result:
            if 'data' in item:
                for data in item['data']:
                    if 'app_id' in data and data['app_id'] == app_id\
                            and 'status' in data and data['status'] == 'valid':
                        return data['user']['username'];
        return 'invalid token'

    def get_token(self, app_id, user):
        """Gets token from database.

        Args:
            app_id (int): application id;
            user (dict): user information;

        Returns:
            token if user exists or None otherwise.
        """
        result = list(self.basedb.get_all('Token'))
        for item in result:
            if 'data' in item:
                for data in item['data']:
                    if 'app_id' in data and data['app_id'] == app_id and\
                        'user' in data and data['user'] == user:
                            return item['token']
        return None

    def access_app(self, app_id, username, password, auth_type=Auth.USERS):
        """Retrieves a user based on a user username/password credential.

        Args:
            auth_type (Auth): the authentification to be searched for;
            app_id (int): application id
            username (str): the inserted username;
            password (str): the inserted password.

        Returns:
            dict: the user corresponding to the authentication match, or None
            otherwise.
        """
        users = self.basedb.get(USER_COLLECTION, APP_KEY, app_id)
        for user in users:  
            if auth_type == Auth.USERS:
                for user_info in user[USER_ITEM]:
                    if user_info['username'] == username and\
                            user_info['password'] == password:
                        del user_info['password']
                        return user_info
        return None

    def get_user(self, app_id, username):
        """Returns user information based on username field. 

        Args:
            username (str): username;

        Returns:
            (dict) user information or None otherwise.
        """
        users = self.basedb.get(USER_COLLECTION, APP_KEY, app_id)
        for user in users:
            for user_info in user[USER_ITEM]:
                if 'username' in user_info and user_info['username'] == username:
                    return user_info
        return None


    def update_user(self, app_id, user_new):
        """Updates user information with `user_new` json content. 
        
        Args: 
            app_id (int): application id
            username (str): the inserted username;
            user_new (dict): user information.

        Return: 
            (dict): user information if exists or None otherwise. 
        """
        if not self.validate(user_new):
            return None
        else:
            username = user_new['username']
            user_old = self.get_user(app_id, username)
            user_new['password'] = self._hash(user_new['password'])
            result = self.basedb.update(USER_COLLECTION, APP_KEY, app_id,
                    USER_ITEM, user_old, user_new)
            return result

    def validate(self, user):
        """Validates user information schema.
        
        Args: 
            user (dict): the user json.

        Returns:
            bool: True if valid or False otherwise.
        """
        SCHEMA = {"type" : "object",
             "properties" : {
                 "username" : {"type" : "string" },
                 "fname" : {"type" : "string"},
                 "lname" : {"type" : "string"},
                 "email" : {"type" : "string"}
            },
             "required" : ["username", "fname", "lname", "email"]
        }
        try:
            validate(user, SCHEMA)
        except ValidationError as err:
            LOG.error('Invalid user information')
            raise Exception('Ivalid user information') from err 
        return True
