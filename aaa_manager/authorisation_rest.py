"""
This file contains the Authorisation REST interface. 
"""
import logging

from aaa_manager import Route
from aaa_manager.authorisation import Authorisation
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
        username = self.request.params['username']
        resource_name = self.request.params['resource_name']
        rule = self.request.params['rule']
        # TODO: aap_id = 2 is hardcoded
        auth = self.authorisation.create(username, resource_name, rule)
        if auth is not None:
            return {'success': 'Rule successfully created.'}
        else:
            return {'error':  'Invalid rule'}
            
