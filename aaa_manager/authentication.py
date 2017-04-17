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
from jsonschema import validate, ValidationError
from enum import Enum
from aaa_manager.basedb import BaseDB
import bcrypt
import base64

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

LOG = logging.getLogger(__name__)
_DEFAULT_DB_HOST = 'mongo'
_DEFAULT_DB_PORT = 27017

USER_COLLECTION = 'users'
APP_KEY = 'app_id'
USER_ITEM = 'auth'
SECRET = '4I3+jNeddexZAgvvh6TS47dZVPp5ezPX+sJ1AW/QvwY='
# expiration is measured in minutes
TOKEN_EXPIRATION = 30 


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

    def _hashpwd(self, data):
        salt = bcrypt.gensalt()
        result = bcrypt.hashpw(data.encode('utf-8'), salt)
        return result.decode('utf-8') 

    def _validatepwd(self, data, pwd):
        return data == bcrypt.hashpw(pwd.encode('utf-8'), data)

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

        if self.verify_token(app_id, user_info['token']) != 'invalid token':
            return self.basedb.remove_list_item(
                    USER_COLLECTION, 
                    APP_KEY, 
                    app_id,
                    USER_ITEM, 
                    {'username': user_info['username']})
        else:
            return 0

    def insert_user(self, app_id, user_info):
        """
        Insert a new user entry on users collection in database.

        Args:
            app_id (int): the app id;
            user_info (dict): the user dict, should contain users and admin's 
            information and credentials.

        
        Returns:
            object: the inserted object or None if error;
            str: 'admin' for repeated admin authentication, or 'users' for 
            repeated username.
        """
        if not self.validate_user(user_info):
            return None, 'invalid user information'
        if not self.validate_pwd(user_info):
            return None, 'invalid password'
        users = self.basedb.get(USER_COLLECTION, APP_KEY, app_id)
        if user_info['username'] == 'admin':
            return None, 'admin'
        auth = copy.deepcopy(user_info)
        auth['password'] = self._hashpwd(auth['password'])
        if not self._is_user_unique(app_id, auth['username']):
            return None, 'users'
        
        email_token = self.generate_token(user_info)
        result_insert = self.insert_email_token(auth['username'], auth['email'], email_token)
        result_email = self.send_email(
                auth['username'], 
                user_info['email'], 
                email_token)

        return self.basedb.insert(USER_COLLECTION, APP_KEY, app_id,
                                        USER_ITEM, auth), ''

    def validate_pwd(self, user_info):
        """
        Validate password against the set of policies:

            - At least 8 characters long;
            - Should be different than username, first and last name, and 
            email;
            - It should include at least 3 of the 4 available types: uppercase 
            letters, lowercase letters, numbers, and symbols.

        Args:
           user_info (dict): user information. 

        Returns:
            bool: True if valid and False otherwise.
        """
        pwd = user_info['password']
        if len(pwd) < 8:
            return False
        if user_info['username'] == pwd\
                or user_info['fname'] == pwd\
                or user_info['lname'] == pwd\
                or user_info['email'] == pwd:
                    return False
        count = 0
        for c in pwd:
            if 'a' <= c <= 'z':
                count = count + 1
                break
        for c in pwd:
            if 'A' <= c <= 'Z':
                count = count + 1
                break
        for c in pwd:
            if '0' <= c <= '9':
                count = count + 1
                break
        symbol = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"
        for c in pwd:
            if c in symbol:
                count = count + 1
                break
        if count < 3:
            return False
        return self.verify_pwd_blacklist(pwd)

    def verify_pwd_blacklist(self, pwd):
        with open('aaa_manager/password_blacklist.txt', 'r') as f:
            blacklist = f.readlines()
            for p in blacklist:
                if pwd == p:
                    return False
            return True

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
        Generate a token that can be used to authenticate user to 
        access app. 

        Args:
            user (dict): user information.

        Returns: 
            str: base64 representation of token.
        """
        #return self._hash(json.dumps(user)+datetime.datetime.now().
        #        strftime("%Y-%m-%d %H:%M:%S"))
        result = bcrypt.hashpw(
                (SECRET+json.dumps(user)).encode('utf-8'), 
                bcrypt.gensalt())
        return base64.b64encode(result).decode('utf-8')
    
    def remove_token(self, token):
        """
        Remove token from DB.

        Args:
            token (str): base64 token

        Returns: 
            obj: mongodb result
        """
        return self.basedb.remove('Token', 'token', token)

    def insert_token(self, app_id, user, token):
        """Insert token into DB.

        Args:
            app_id (int): application id;
            user (dict): user information;
            token (str): hexidecimal token.

        Returns: 
            obj: mongodb result
        """
        return self.basedb.insert('Token', 'token', token, 'data', 
                {
                    'app_id': app_id, 
                    'user': user, 
                    'created': datetime.datetime.now()
                    })
    
    def insert_email_token(self, username, email, token):
        """Insert email token into DB.

        Args:
            username (str): username;
            email (str): user email address;
            token (str): user email token.

        Returns: 
            obj: mongodb result
        """
        return self.basedb.insert('EmailToken', 'email', email, 'data', 
                {
                    'token': token, 
                    'username': username, 
                    'created': datetime.datetime.now(),
                    'valid': False
                    })

    def verify_token(self, app_id, token):
        """Verify token validity.

        Args:
            app_id (int): application id
            token (str): base64 token

        Returns:
            str: username corresponding to token if valid, 
            'invalid token' otherwise
        """
        result = list(self.basedb.get('Token', 'token', token))
        for item in result:
            if 'data' in item:
                for data in item['data']:
                    if 'app_id' in data\
                            and data['app_id'] == app_id\
                            and 'created' in data\
                            and (datetime.datetime.now() - datetime.timedelta(minutes=TOKEN_EXPIRATION) < data['created']):
                        LOG.info('#### %s' % (datetime.datetime.now() - datetime.timedelta(minutes=TOKEN_EXPIRATION) < data['created']))
                        LOG.info('#### created: %s' % data['created'])
                        return data['user']['username']
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
            dict: the user corresponding to the authentication match, 
            or None
            otherwise.
        """
        users = self.basedb.get(USER_COLLECTION, APP_KEY, app_id)
        for user in users:  
            if auth_type == Auth.USERS:
                for user_info in user[USER_ITEM]:
                    if user_info['username'] == username:
                        hashpwd = user_info['password'] 
                        if self._validatepwd(hashpwd.encode('utf-8'), password):
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
                if 'username' in user_info\
                        and user_info['username'] == username:
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
        try:
            if self.verify_token(app_id, user_new['token']) != 'invalid token':
                userelem = {}
                res = self.basedb.get(USER_COLLECTION, APP_KEY, app_id)
                for item in list(res):
                    for elem in item['auth']:
                        if elem['username'] == user_new['username']:
                            userelem = elem
                resdel = self.delete_user(app_id, user_new)
                del user_new['token']
                if resdel > 0:
                    userelem['fname'] = user_new['fname']
                    userelem['lname'] = user_new['lname']
                    userelem['email'] = user_new['email']
                    LOG.info('#### userelem: %s' % userelem)
                    resinsert = self.basedb.insert(
                            USER_COLLECTION, 
                            APP_KEY, 
                            app_id,
                            USER_ITEM, 
                            userelem)
                    if resinsert is not None:
                        return 1
        except Exception as err:
            LOG.error('Error while updating user information')
            raise Exception('Error while updating user information') from err 
        return 0
    
    def change_password(self, app_id, user_new):
        """Updates user information with `user_new` json content. 
        
        Args: 
            app_id (int): application id
            username (str): the inserted username;
            user_new (dict): user information.

        Return: 
            (dict): user information if exists or None otherwise. 
        """
        try:
            if self.verify_token(app_id, user_new['token']) != 'invalid token':
                userelem = {}
                res = self.basedb.get(USER_COLLECTION, APP_KEY, app_id)
                oldpassword = ""
                for item in list(res):
                    for elem in item['auth']:
                        if elem['username'] == user_new['username']:
                            userelem = elem
                            oldpassword = elem['password']
                oldpwd = user_new['oldpwd'] 
                if self._validatepwd(oldpassword.encode('utf-8'), oldpwd):
                    resdel = self.delete_user(app_id, user_new)
                    del user_new['token']
                    if resdel > 0:
                        newpassword = self._hashpwd(user_new['newpwd'])
                        userelem['password'] = newpassword
                        resinsert = self.basedb.insert(
                                USER_COLLECTION,
                                APP_KEY,
                                app_id, 
                                USER_ITEM,
                                userelem)
                        if resinsert is not None:
                            return 1
        except Exception as err:
            LOG.error('Error while changing password.')
            raise Exception('Error while changing password.') from err 
        return 0

    def validate_user(self, user):
        """Validates user information schema.
        
        Args: 
            user (dict): the user json.

        Returns:
            bool: True if valid or False otherwise.
        """
        SCHEMA = {"type" : "object",
             "properties" : {
                 "username" : {
                     "type" : "string",
                     "minLength": 1,
                     "maxLength": 50
                     },
                 "fname" : {
                     "type" : "string",
                     "minLength": 1,
                     "maxLength": 50
                     },
                 "lname" : {
                     "type" : "string",
                     "minLength": 1,
                     "maxLength": 50
                     },
                 "email" : {
                     "type" : "string",
                     "pattern": "[^@]+@[^@]+\.[^@]+",
                     }
            },
             "required" : ["username", "fname", "lname", "email"]
        }
        try:
            validate(user, SCHEMA)
        except ValidationError as err:
            LOG.error('Invalid user information')
            raise Exception('Invalid user information') from err 
        return True

    def email_confirmation(self, username, email, token):
        """
        Verifies if given token is valid.

        Args: 
            username (str): username;
            email (str): user email;
            token (str): email token encoded in base64.

        Returns:
            bool: True if valid and False otherwise.
        """
        
        self.basedb.insert('EmailToken', 'email', email, 'data', 
                {
                    'token': token, 
                    'username': username, 
                    'validated': datetime.datetime.now(),
                    'valid': True
                    })
        return True
      
    def verify_email(self, username, email):
        """
        Verifies if given token is valid.

        Args: 
            username (str): username;
            email (str): user email;
            token (str): email token encoded in base64.

        Returns:
            bool: True if valid and False otherwise.
        """
        result = list(self.basedb.get('EmailToken', 'email', email))
        for item in result:
            if 'data' in item:
                data = item['data']
                if data['valid']: 
                    return True
        return False

    def send_email(self, username, email, token):
        # me == the sender's email address
        # you == the recipient's email address
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'email confirmation'
        msg['From'] = 'bigsea@bigsea.com'
        msg['To'] = email

        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
        html = """\
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               How are you?<br>
               Here is the <a href="https://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>
        """

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via our own SMTP server.
        #s = smtplib.SMTP('localhost')
        #s.send_message(msg)
        #s.quit()

