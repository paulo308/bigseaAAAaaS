"""
This file contains the Authorisation REST interface. 
"""
import logging

from aaa_manager import Route
from aaa_manager.infra import Infra
from aaa_manager.token import Token
from aaa_manager.authentication import AuthenticationManager, Auth
from pyramid.view import view_config

LOG = logging.getLogger(__name__)


class InfraRestView:
    """
    Implements infra REST API.
    """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']
        self.infra = Infra()
        self.auth = AuthenticationManager() 
        self.token = Token()

    @view_config(route_name=Route.INSERT_DATA_INFRA,
                 request_method='POST',
                 renderer='json')
    def create(self):
        """ 
        This method is called from **/engine/api/insert_data_infra**.
        This method is used to create infra association.

        Arguments:
            username (str): the username;
            principal (dict): principal;
            secret (dict): secret.

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            infra_info = {
                    'principal': self.request.params['principal'],
                    'secret': self.request.params['secret']
                    }
            #token = self.request.params['token']
            #usr = self.token.verify_token(2, token)
            #if usr != 'invalid token' and usr == username:
            auth = self.infra.create(username, infra_info)
            if auth is not None:
                return {'success': 'Infra data successfully created.'}
            else:
                return {'error':  'Invalid infra data.'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
            
    @view_config(route_name=Route.CHECKIN_DATA_INFRA,
                 request_method='POST',
                 renderer='json')
    def read(self):
        """ 
        This method is called from **/engine/api/checkin_data_infra**.
        This method is used to insert infra credentials.

        Arguments:
            username (str): the username;
            principal (str): password.

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            data (dict): object with infra data;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            usr = self.request.params['username']
            pwd = self.request.params['pwd']
            user, msg = self.auth.access_app(
                    2, 
                    usr, 
                    pwd, 
                    Auth.USERS)
            if user is not None:
                result = self.infra.read(usr)
                if result is not None:
                    return {'success': 'Infra data successfully read.',
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
