"""
This file contains the Authorisation REST interface. 
"""
import logging

from aaa_manager import Route
from aaa_manager.emails import Emails
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
        username = self.request.params['username']
        email_info = self.request.params['email_info']
        auth = self.emails.create(username, email_info)
        if auth is not None:
            return {'success': 'Email association successfully created.'}
        else:
            return {'error':  'Invalid email.'}
            
