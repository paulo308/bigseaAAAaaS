"""Main module of backend, where controller and view paths are defined"""
import logging

from aaa_manager import Route
from aaa_manager.authentication import AuthenticationManager, Auth
from pyramid.view import view_config

log = logging.getLogger(__name__)


class RestView:
    """ Implements the main REST API """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']
        self.authentication = AuthenticationManager()

    @view_config(route_name=Route.CHECKIN,
                 request_method='POST',
                 renderer='string')
    def checkin(self):
        """ This method is called from **/engine/api/checkin**.
        """
        log.info('entrou')
        #result = self.authentication.insert_user(1, {'infra': {'username': 'testeinfra', 'password': '4321'}, 'users': [{'username': 'teste', 'password': '1234'}]})
        #log.info('result: %s' % result[0])

        #if self.request.params['user'] == 'teste' and \
        #                self.request.params['pwd'] == '1234':
        usr = self.request.params['user']
        pwd = self.request.params['pwd']
        log.info('usr: %s' % usr)
        log.info('pwd: %s' % pwd)
        result = self.authentication.access_app(usr, self.authentication._hash_password(pwd), Auth.USERS)
        log.info('result: %s' % result)
        if result is not None:
            # REST API logged in
            log.info('#### authenticated!!!!')
            return {}
        else:
            return 401
        return {}

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
