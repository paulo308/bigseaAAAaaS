"""
This file contains the Authorisation REST interface. 
"""
import logging

from aaa_manager import Route
from aaa_manager.emails import Emails
from aaa_manager.token import Token
from aaa_manager.authentication import AuthenticationManager
from pyramid.view import view_config

LOG = logging.getLogger(__name__)


class EmailsRestView:
    """
    Implements emails REST API.
    """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']
        self.emails = Emails()
        self.token = Token()

    @view_config(route_name=Route.CREATE_EMAIL,
                 request_method='POST',
                 renderer='json')
    def create(self):
        """ 
        This method is called from **/engine/api/create_email_data**.
        This method is used to create email association.

        Arguments:
            username (str): the username;
            email_info (dict): email information.

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            email_info = {'email': self.request.params['email']}
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                auth = self.emails.create(username, email_info)
                if auth is not None:
                    return {'success': 'Email association successfully created.'}
                else:
                    return {'error':  'Invalid email.'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
            
    @view_config(route_name=Route.READ_EMAILS,
                 request_method='POST',
                 renderer='json')
    def read(self):
        """ 
        This method is called from **/engine/api/read_emails**.
        This method is used to read email association.

        Arguments:
            username (str): the username;

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            data (dict): object with emails;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                result = self.emails.read_all(username)
                if result is not None:
                    return {'success': 'Email association successfully read.',
                            'data': result}
                else:
                    return {'error':  'Invalid username.'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
    
    @view_config(route_name=Route.DELETE_EMAIL,
                 request_method='POST',
                 renderer='json')
    def delete(self):
        """ 
        This method is called from **/engine/api/delete_email**.
        This method is used to delete association.

        Arguments:
            username (str): the username;
            email (dict): email information.

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            data (dict): object with emails;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            email = self.request.params['email']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                result = self.emails.delete(username, email)
                if result is not None:
                    return {'success': 'Email association successfully deleted.'}
                else:
                    return {'error':  'Invalid username.'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
