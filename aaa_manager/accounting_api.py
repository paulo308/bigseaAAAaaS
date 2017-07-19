"""
This file contains the Authorisation REST interface. 
"""
import logging
import json

from aaa_manager import Route
from aaa_manager.token import Token
from aaa_manager.accounting import Accounting
from aaa_manager.authentication import AuthenticationManager
from pyramid.view import view_config

LOG = logging.getLogger(__name__)


class AccountingRestView:
    """
    Implements the main REST API.
    """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']
        self.accounting = Accounting()
        self.authentication = AuthenticationManager()
        self.token = Token()

    @view_config(route_name=Route.READ_ACCOUNTING,
                 request_method='POST',
                 renderer='json')
    def get(self):
        """ 
        This method is called from **/engine/api/get_accounting_data**.
        This method is called in order to get accounting information from user.

        Arguments:
            username (str): the username;

        Returns:
            success (bool): True if sucessfully get accounting information and 
            False otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                data = self.accounting.get(username)
                if data is not None:
                    return {'success': 'User accounting information read successfully.',
                            'data': json.dumps(data)}
                else:
                    return {'error':  'Accounting information not found.'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
            
