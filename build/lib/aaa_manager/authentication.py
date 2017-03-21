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
        Verifies if the admin username on app data is unique.

        Args:
            app_id (int): the app key
            username (str): the username being tested

        Returns:
            boolean: False if the admin username is already present, True
                otherwise
        """
        users = list(self.basedb.get(USER_COLLECTION, APP_KEY, app_id))
        for elem in users:
            for elem_item in elem[USER_ITEM]:
                if elem_item['admin']['username'] == username:
                    return False
        return True


    def _is_user_unique(self, app_id, username):
        """Verifies if the username on a app data is unique

        Args:
            app_id (int): the app key
            username (str): the username being tested

        Returns:
            boolean: False if the user username is already present, True
                otherwise
        """
        users = list(self.basedb.get(USER_COLLECTION, APP_KEY, app_id))
        for user in users:
            for elem in user[USER_ITEM]:
                if elem['username'] == username:
                    return False
        return True

    def _hash(self, data):
        """Hashes a string using SHA-512.

        Args:
            password (str): the password to be hashed

        Returns:
            str: the digest of the hashed password in hexadecimal digits
        """
        return hashlib.sha512(data.encode()).hexdigest()

    def get_all_users(self):
        """Get all users

        Returns:
            dict: all users data
        """
        users = []
        for user in self.basedb.get_all(USER_COLLECTION):
            users.append(self._format_user_dict(user))
        return users

    def delete_user(self, app_id, username):
        """
        Deletes a new user entry on users collection in DB

        Args:
            app_id (int): the app id
            username (dict): the username

        Returns:
            object: The inserted object or None on failure
            str: 'admin' if the cause of failure was repeated admin authentication, 'users' for a non unique username, 'id' if the app_id already exists, 'username' for duplicated username on the auth_info
        """
        users = self.basedb.get(USER_COLLECTION, APP_KEY, app_id)
        auth = copy.deepcopy(user_info)
        return self.basedb.remove_item(USER_COLLECTION, APP_KEY, app_id,
                                        USER_ITEM, auth), ''

    def insert_user(self, app_id, user_info):
        """
        Inserts a new user entry on users collection in DB

        Args:
            app_id (int): the app id
            auth_info (dict): the user dict, should contain the users and the admin's data, and a username/password pair

        
        Returns:
            object: The inserted object or None on failure
            str: 'admin' if the cause of failure was repeated admin authentication, 'users' for a non unique username, 'id' if the app_id already exists, 'username' for duplicated username on the auth_info
        """
        users = self.basedb.get(USER_COLLECTION, APP_KEY, app_id)
        if user_info['username'] == 'admin':
            return None, 'admin'
        auth = copy.deepcopy(user_info)
        auth['password'] = self._hash(auth['password'])
        LOG.info('#### users: %s' % list(users))
        LOG.info('#### auth: %s' % auth)
        if not self._is_user_unique(app_id, auth['username']):
            return None, 'users'

        return self.basedb.insert(USER_COLLECTION, APP_KEY, app_id,
                                        USER_ITEM, auth), ''

    def remove_app(self, app_id):
        """Removes a user entry on users collection in DB

        Args:
            app_id (int): the user key

        Returns:
            The kdb remove operation result
        """
        return self.basedb.remove(USER_COLLECTION, APP_KEY, app_id)


    def generate_token(self, user):
        """Generates a token that can be used to authenticate user to access
        app. 

        Args:
            user (dict): user information

        Returns: 
            str: hexadecimal representation of token
        """
        return self._hash(json.dumps(user)+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def remove_token(self, token):
        """Remove token from DB.

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
        """Get token from database

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
        """Retrieves a user based on a user username/password pair

        Args:
            auth_type (Auth): the authentification to be searched for
            username (str): the inserted username
            password (str): the inserted password

        Returns:
            dict: the user corresponding to the authentication pair match,
                or None if any
        """
        users = self.basedb.get(USER_COLLECTION, APP_KEY, app_id)
        for user in users:
            if auth_type == Auth.USERS:
                for user_info in user[USER_ITEM]:
                    if user_info['username'] == username and user_info['password'] == \
                        password:
                        del user_info['password']
                        return user_info
        return None
