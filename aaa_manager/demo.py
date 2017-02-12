from aaa_manager.route import Route
from pyramid.view import view_config
import logging
import json
import jsonschema
#from evaluation_engine.exceptions import InvalidJsonError
#from evaluation_engine.model.internal_scan import InternalScan
#from evaluation_engine.model.connection_data import ConnectionData
#from evaluation_engine.tasks.connection_data_analysis import ConnectionDataDisplayTask

log = logging.getLogger(__name__)

class DemoWebView:
    """ Implements the demo web interface view """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings

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

    @view_config(route_name=Route.WEB_CHECKOUT,
                 renderer='logout.jinja2')
    def checkout(self):
        """This method is called from **/web/checkout**"""
        return ''


class DemoRestView:
    """ Implements the demo REST API """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']

    @view_config(route_name=Route.GET_CHECKIN, renderer='json')
    def get_checkin_state(self):
        """
        Retrives the checkin state.

        Note:
            This method is called from **/json/get_checkin_state**.
            Currently this is called by ajax

        Returns:
            (dict): containing the checkin state
        """

        # Dummy data to test webpage (create device info)
        self._settings['data'] = json_body
        return {}

        
    @view_config(route_name=Route.GET_CHECKOUT, renderer='json')
    def checkout_state(self):
        """
        Retrives the checkout.

        Note:
            Used by the web interface from 
            **/json/get_checkout**

        Returns:
            (dict): containing the checkout state
        """
        self._settings['data'] = json_body
        return {}
