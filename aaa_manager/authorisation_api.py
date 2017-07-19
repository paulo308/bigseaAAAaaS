"""
This file contains the Authorisation REST interface. 
"""
import logging

from aaa_manager import Route
from aaa_manager.token import Token
from aaa_manager.authorisation import Authorisation
from aaa_manager.authentication import AuthenticationManager
from pyramid.view import view_config


LOG = logging.getLogger(__name__)


class AuthorisationRestView:
    """
    Implements the main REST API.
    """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']
        self.authorisation = Authorisation()
        self.authentication = AuthenticationManager()
        self.token = Token()

    @view_config(route_name=Route.CREATE_AUTHORISATION,
                 request_method='POST',
                 renderer='json')
    def create(self):
        """ 
        This method is called from **/engine/api/create_authorisation_data**.
        This method is used to create authorisation rules.

        Arguments:
            username (str): the username;
            resource_name (str): the resource name;
            rule (dict): rule.

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            resource_category = self.request.params['resource_category']
            resource_name = self.request.params['resource_name']
            max_used = self.request.params['max']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                auth = self.authorisation.create(
                        username, 
                        resource_category, 
                        resource_name, 
                        max_used)
                if auth is not None:
                    return {'success': 'Rule successfully created.'}
                else:
                    return {'error':  'Invalid rule'}
            else:
                return {'error': 'Invalid token'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
            
    @view_config(route_name=Route.USE_RESOURCE,
                 request_method='POST',
                 renderer='json')
    def use(self):
        """ 
        This method is called from **/engine/api/use_resource_data**.
        This method is called in order to get authorisation to use a determined 
        resource.

        Arguments:
            username (str): the username;
            resource_name (str): the resource name.

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            resource_name = self.request.params['resource_name']
            resource_category = self.request.params['resource_category']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                auth = self.authorisation.use_resource(
                        username, 
                        resource_name, 
                        resource_category)
                if auth is not None:
                    return {'success': 'User is authorised.'}
                else:
                    return {'error':  'User is not authorised.'}
            else:
                return {'error': 'Invalid token'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
    
    @view_config(route_name=Route.READ_AUTHORISATION,
                 request_method='POST',
                 renderer='json')
    def read_authorisation(self):
        """ 
        This method is called from **/engine/api/read_authorisation**.
        This method is called in order to read authorisation rule.

        Arguments:
            username (str): the username;
            resource_name (str): the resource name.
            resource_category (str): the resource type.

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        LOG.info('entrou')
        msg = ''
        try:
            LOG.info('params: %s' % self.request.params)
            username = self.request.params['username']
            resource_name = self.request.params['resource_name']
            resource_category = self.request.params['resource_category']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                auth = self.authorisation.read(
                        username, 
                        resource_name, 
                        resource_category)
                if auth is not None:
                    return {'success': 'Rule successfully read.'}
                else:
                    return {'error':  'Rule not found.'}
            else:
                return {'error': 'Invalid token'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
    
    @view_config(route_name=Route.READ_AUTHORISATIONS,
                 request_method='POST',
                 renderer='json')
    def read_authorisations(self):
        """ 
        This method is called from **/engine/api/read_authorisations**.
        This method is called in order to read authorisation rules.

        Arguments:
            username (str): the username;

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                auths = self.authorisation.read_authorisations(username)
                if auths is not None:
                    return {'success': 'Rule successfully read.',
                            'data': auths}
                else:
                    return {'error':  'Rule not found.'}
            else:
                return {'error': 'Invalid token'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}



            
    @view_config(route_name=Route.UPDATE_AUTHORISATION,
                 request_method='POST',
                 renderer='json')
    def update(self):
        """ 
        This method is called from **/engine/api/update_authorisation**.
        This method is called in order to update authorisation rule.

        Arguments:
            username (str): the username;
            resource_name (str): the resource name.

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            resource_name = self.request.params['resource_name']
            resource_category = self.request.params['resource_category']
            max_allowed = self.request.params['max_allowed']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                auth = self.authorisation.update(
                        username, 
                        resource_name, 
                        resource_category,
                        max_allowed)
                if auth is not None:
                    return {'success': 'Rule successfully updated.'}
                else:
                    return {'error':  'Rule not found.'}
            else:
                return {'error': 'Invalid token'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
            
    @view_config(route_name=Route.DELETE_AUTHORISATION,
                 request_method='POST',
                 renderer='json')
    def delete(self):
        """ 
        This method is called from **/engine/api/delete_authorisation**.
        This method is called in order to delete rule.

        Arguments:
            username (str): the username;
            resource_name (str): the resource name.

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            resource_name = self.request.params['resource_name']
            resource_category = self.request.params['resource_category']
            max_allowed = self.request.params['max_allowed']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                auth = self.authorisation.delete(
                        username, 
                        resource_name, 
                        resource_category)
                if auth is not None:
                    return {'success': 'Rule successfully deleted.'}
                else:
                    return {'error':  'Rule not found.'}
            else:
                return {'error': 'Invalid token'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
