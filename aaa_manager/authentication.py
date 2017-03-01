"""A interface for accessing users collection on DB"""
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
USER_KEY = 'app_id'
USER_ITEM = 'auth'


class Auth(Enum):
    """ Authentication being verified """
    ADMIN = 0
    INFRA = 1
    USERS = 2

class AuthenticationManager:
    """ Provides an interface to access and manipulate user data collections"""

    def __init__(self, host=_DEFAULT_DB_HOST, port=_DEFAULT_DB_PORT):
        self.host = host
        self.port = port
        self.basedb = BaseDB(host, port)

    def _format_user_dict(self, user):
        return {
            USER_KEY: user[USER_KEY],
            USER_ITEM: user[USER_ITEM][0]
        }

    def _is_infra_unique(self, app_id, username):
        """Verifies if the infra username on a user data is unique

        Args:
            app_id (int): the user key
            username (str): the username being tested

        Returns:
            boolean: False if the infra username is already present, True
                otherwise
        """
        users = self.get_all_users()
        for elem in users:
            if elem[USER_KEY] != app_id:
                if elem[USER_ITEM]['infra']['username'] == username:
                    return False
        return True


    def _is_user_unique(self, app_id, username):
        """Verifies if the username on a user data is unique

        Args:
            app_id (int): the user key
            username (str): the username being tested

        Returns:
            boolean: False if the user username is already present, True
                otherwise
        """
        users = self.get_all_users()
        for user in users:
            # Verifies repetition for the userlist of the same app
            if user[USER_KEY] == app_id:
                count = 0
                for elem in user[USER_ITEM]['users']:
                    if elem['username'] == username:
                        count += 1
                if count > 1:
                    return False
            # Verifies others users
            else:
                for elem in user[USER_ITEM]['users']:
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

    def insert_user(self, app_id, auth_info):
        """Inserts a new user entry on users collection in DB

        Args:
            app_id (int): the user key
            auth_info (dict): the user dict, should contain the users and
                the infra's data, and a username/password pair

        Returns:
            object: The inserted object or None on failure
            str: 'infra' if the cause of failure was repeated infra
                authentication, 'users' for a non unique username,
                'id' if the app_id already exists,
                'username' for duplicated username on the auth_info
        """
        users = self.get_all_users()
        for user in users:
            if user[USER_KEY] == app_id:
                return None, 'id'
        if (len(set([user['username'] for user in auth_info['users']])) <
            len(auth_info['users'])):
            return None, 'username'
        if not self._is_infra_unique(app_id,
                                      auth_info['infra']['username']):
            return None, 'infra'
        auth = copy.deepcopy(auth_info)
        for user in auth['users']:
            user['password'] = self._hash(user['password'])
            if not self._is_user_unique(app_id, user['username']):
                return None, 'users'

        auth['infra']['password'] = self._hash(
            auth['infra']['password'])

        return self.basedb.insert(USER_COLLECTION, USER_KEY, app_id,
                                        USER_ITEM, auth), ''

    def remove_user(self, app_id):
        """Removes a user entry on users collection in DB

        Args:
            app_id (int): the user key

        Returns:
            The kdb remove operation result
        """
        return self.basedb.remove(USER_COLLECTION, USER_KEY, app_id)

    def get_user(self, app_id):
        """Gets the infra info for a given user id

        Args:
            app_id (int): the user key

        Returns:
            dict: the dict containing the retrieved result, or None if not found
        """

        ret = list(self.basedb.get(USER_COLLECTION, USER_KEY, app_id))

        if len(ret) == 0:
            return None
        else:
            return self._format_user_dict(ret[0])

    def update_user(self, app_id, auth_old_info, auth_new_info):
        """Updates a user entry on users collection in DB

        Args:
            app_id (int): the user key
            auth_old_info (dict): the current item part of the user data
            auth_new_info (dict): the modified item part of the user data

        Returns:
            int: the number of elements modified, None if failure
            str: 'infra' if the cause of failure was repeated infra
                authentication or 'user' for a not unique username
        """
        if not self._is_infra_unique(app_id,
                                      auth_new_info['infra']['username']):
            return None, 'infra'
        auth = copy.deepcopy(auth_new_info)
        for user in auth['users']:
            user['password'] = self._hash(user['password'])
            if not self._is_app_unique(app_id, user['username']):
                return None, 'users'

        auth['infra']['password'] = self._hash(
            auth['infra']['password'])
        return self.basedb.update(USER_COLLECTION, USER_KEY, app_id,
                                        USER_ITEM, auth_old_info,
                                        auth), ''


    def verify_infra_credential(self, app_id, username, password):
        """Verifies if the given infra username/password pair matches the
        expected for a given user

        Args:
            app_id (int): the user key
            username (str): the inserted username
            password (str): the inserted password

        Returns:
            boolean: if the username and password are a match or not
            str: a string informing 'match', 'user not found' or
                'username and/or password do not match' to describe the result
        """
        data = self.get_user(app_id)
        status = 'user not found'
        if data is not None:
            data = data[USER_ITEM]['infra']
            if data['username'] == username and \
                data['password'] == self._hash(password):
                return True, 'match'
            else:
                status = 'username and/or password do not match'
        return False, status

    def generate_token(self, user):
        return self._hash(json.dumps(user)+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def insert_token(self, app_id, user, token):
        return self.basedb.insert('Token', 'token', token, 'data', {'app_id': app_id, 'user': user})

    def verify_token(self, app_id, user, token):
        LOG.info('#### verify_token %s %s %s' % (app_id, user, token))
        result = list(self.basedb.get('Token', 'token', token))
        LOG.info('#### result: %s' % result)
        for item in result:
            LOG.info('#### item: %s' % item)
            if 'data' in item:
                for data in item['data']:
                    LOG.info('#### data: %s' % data)
                    if 'app_id' in data and data['app_id'] == app_id and\
                        'user' in data and data['user'] == user:
                            return True;
        return False

    def get_token(self, app_id, user):
        result = list(self.basedb.get_all('Token'))
        for item in result:
            if 'data' in item:
                for data in item['data']:
                    if 'app_id' in data and data['app_id'] == app_id and\
                        'user' in data and data['user'] == user:
                            return item['token']
        return None

    def access_app(self, username, password, auth_type=Auth.USERS):
        """Retrieves a user based on a user username/password pair

        Args:
            auth_type (Auth): the authentification to be searched for
            username (str): the inserted username
            password (str): the inserted password

        Returns:
            dict: the user corresponding to the authentication pair match,
                or None if any
        """
        users = self.get_all_users()
        for user in users:
            if auth_type == Auth.USERS:
                for user in user[USER_ITEM]['users']:
                    if user['username'] == username and user['password'] == \
                        password:
                        return user
            else:
                if user[USER_ITEM]['infra']['username'] == username and \
                        user[USER_ITEM]['infra']['password'] == \
                        password:
                    return user
        return None

    def get_user_id(self, username):
        """Retrieves a user id by identifing the user

        Args:
            username (str): the username to be used

        Returns:
            int: the user id, or None if not found
        """
        users = self.get_all_users()
        for user in users:
            for user in user[USER_ITEM]['users']:
                if user['username'] == username:
                    return user[USER_KEY]
            infra = user[USER_ITEM]['infra']
            if infra['username'] == username:
                return user[USER_KEY]
        return None

