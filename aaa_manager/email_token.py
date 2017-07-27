
import logging
import datetime
import copy
from aaa_manager.token import Token
from aaa_manager.basedb import BaseDB
from aaa_manager.send_email import SendEmail

LOG = logging.getLogger(__name__)
    
class EmailToken:

    def __init__(self):
        self.token = Token()
        self.basedb = BaseDB()
        self.sendEmail = SendEmail()
        pass

    def insert_email_token(self, username, email, token, valid):
        result = self.basedb.insert('EmailToken', 'email', email, 'data', 
                {
                    'token': token, 
                    'username': username, 
                    'validated': datetime.datetime.now(),
                    'valid': valid
                    })
        return result

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
        result = False
        data = self.basedb.get('EmailToken', 'email', email)
        for item in data:
            LOG.info('item: %s' % item)
            for elem in item['data']:
                if elem['token'] == token:
                    new_elem = copy.deepcopy(elem) 
                    new_elem['valid'] = True
                    res = self.basedb.remove_list_item(
                            'EmailToken',
                            'email',
                            email,
                            'data',
                            elem)
                    res = self.basedb.insert(
                            'EmailToken',
                            'email',
                            email,
                            'data',
                            new_elem)
                    result = True
        return result

    def send_email_token(self, username, email):
        """
        Send email with new generated token.
        """
        token = self.token.generate_token(username+email)
        self.insert_email_token(username, email, token, False)
        self.sendEmail.send_email_with_token(username, email, token)
        return token


    def verify_email(self, username, email):
        """
        Verifies if given token is valid.
        TODO: must grant that only the last one is valid.

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
                for elem in data:
                    if elem['valid'] == True and elem['username'] == username: 
                        return True
        return False
