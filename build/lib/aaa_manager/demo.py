from aaa_manager.route import Route
from pyramid.view import view_config
from aaa_manager.authentication import AuthenticationManager
import logging
import json
import jsonschema

log = logging.getLogger(__name__)

class DemoWebView:
    """ Implements the demo web interface view """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self.authentication = AuthenticationManager()

    @view_config(route_name=Route.WEB,
                 renderer='home.jinja2')
    @view_config(route_name=Route.HOME,
                 renderer='home.jinja2')
    def home(self):
        """This method is called from **/** or **/web**"""
        return ''

    @view_config(route_name=Route.WEB_CHECKIN,
                 renderer='login.jinja2')
    def checkin(self):
        """This method is called from **/web/checkin**"""
        return ''

    @view_config(route_name=Route.WEB_SIGNUP,
                 renderer='signup.jinja2')
    def signup(self):
        """This method is called from **/web/signup**"""
        return ''


class DemoRestView:
    """ Implements the demo REST API """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']

    @view_config(route_name=Route.GET_CHECKIN, renderer='json')
    def checkin_data(self):
        """
        Retrives the checkin state.

        Note:
            This method is called from **/json/get_checkin_state**.
            Currently this is called by ajax

        Returns:
            (dict): containing the checkin state
        """
        self._settings['data'] = json_body
        return {}

        
    @view_config(route_name=Route.GET_SIGNUP, renderer='json')
    def signup_data(self):
        """
        Retrives the checkout.

        Note:
            Used by the web interface from 
            **/json/get_signup**

        Returns:
            (dict): containing the checkout state
        """
        self._settings['data'] = json_body
        return {}
