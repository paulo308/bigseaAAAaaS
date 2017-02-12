"""Main module of backend, where controller and view paths are defined"""
import logging

#from evaluation_engine.model.connection_data import ConnectionData
#from evaluation_engine.model.internal_scan import InternalScan
#from evaluation_engine.model.mobile_data import MobileDataRequest
#from evaluation_engine.tasks.internal_scan_analysis import InternalScanAnalysisTask
#from evaluation_engine.tasks.connection_data_analysis import ConnectionDataDisplayTask
#from evaluation_engine.tasks.mobile_analysis import MobileRequest, MobileTask
from aaa_manager import Route
from pyramid.view import view_config

log = logging.getLogger(__name__)


class RestView:
    """ Implements the main REST API """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']

    @view_config(route_name=Route.CHECKIN,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def checkin(self):
        """ This method is called from **/engine/api/checkin**.
        """
        if self.request.params['user'] == 'dc' and \
                        self.request.params['password'] ==\
                        'egJz7Rqw7tsJOLLE9UaXaSN09OAhNawq8HhZg7KrGmM=':
            # REST API logged in
            return {}
        else:
            return 401

    @view_config(route_name=Route.CHECKOUT,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def checkout(self):
        """ This method is called from **/engine/api/checkout**.
        """
        int_scan = Checkout(self.request.json_body)
        if self.request.params['user'] == 'dc' and\
                        self.request.params['password'] ==\
                        'egJz7Rqw7tsJOLLE9UaXaSN09OAhNawq8HhZg7KrGmM=':
            # REST API logged out
            return {}
        else:
            return 401
