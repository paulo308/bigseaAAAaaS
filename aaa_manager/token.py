
import logging
import bcrypt
import base64
import json
import datetime
from aaa_manager.basedb import BaseDB

SECRET = '4I3+jNeddexZAgvvh6TS47dZVPp5ezPX+sJ1AW/QvwY='

# expiration is measured in minutes
TOKEN_EXPIRATION = 720 
TOKEN_EXPIRATION_STAYIN = 10080 

LOG = logging.getLogger(__name__)

class Token:

    def __init__(self):
        self.basedb = BaseDB()
    
    def get_token(self, user):
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
                    if 'user' in data and data['user'] == user:
                            return item['token']
        return None

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
    

    def verify_token(self, app_id, token):
        """Verify token validity.

        Args:
            app_id (int): application id;
            token (str): base64 token.

        Returns:
            str: username corresponding to token if valid, 
            'invalid token' otherwise
        """
        result = self.read_user_info(app_id, token)
        if result != 'invalid token':
            return result['username']
        else:
            return 'invalid token'


    def read_user_info(self, app_id, token):
        """Read user information.

        Args:
            app_id (int): application id;
            token (str): base64 token.

        Returns:
            str: username corresponding to token if valid, 
            'invalid token' otherwise
        """
        result = list(self.basedb.get('Token', 'token', token))
        for item in result:
            if 'data' in item:
                for data in item['data']:
                    if 'app_id' in data and data['app_id'] == app_id\
                            and 'created' in data and\
                            'user' in data and 'stayin' in data['user']:
                        if (data['user']['stayin'] == True\
                                and (datetime.datetime.now() - datetime.timedelta(minutes=TOKEN_EXPIRATION_STAYIN) < data['created']))\
                                or (data['user']['stayin'] == False\
                                and (datetime.datetime.now() - datetime.timedelta(minutes=TOKEN_EXPIRATION) < data['created'])):
                            LOG.info('#### %s' % (datetime.datetime.now() - datetime.timedelta(minutes=TOKEN_EXPIRATION) < data['created']))
                            LOG.info('#### %s' % (datetime.datetime.now() - datetime.timedelta(minutes=TOKEN_EXPIRATION_STAYIN) < data['created']))
                            LOG.info('#### created: %s' % data['created'])
                            LOG.info('#### stayin: %s' % data['user']['stayin'])
                            return data['user']
                    if 'stayin' not in data['user']:
                        if (datetime.datetime.now() - datetime.timedelta(minutes=TOKEN_EXPIRATION) < data['created']):
                            return data['user']
        return 'invalid token'

