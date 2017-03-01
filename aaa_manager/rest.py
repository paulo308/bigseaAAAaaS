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
        #result = self.authentication.insert_user(1, {'infra': {'username': 'testeinfra', 'password': '4321'}, 'users': [{'username': 'teste', 'password': '1234'}]})
        #log.info('result: %s' % result[0])

        usr = self.request.params['user']
        pwd = self.request.params['pwd']
        log.info('usr: %s' % usr)
        log.info('pwd: %s' % pwd)
        user = self.authentication.access_app(usr, self.authentication._hash(pwd), Auth.USERS)
        token = self.authentication.generate_token(user)
        log.info('user: %s' % user)
        log.info('token: %s' % token)
        response = self.authentication.insert_token(1, user, token)
        log.info('response: %s' % response)
        verify = self.authentication.verify_token(1, user, token)
        log.info('verify: %s' % verify)
        
        if user is not None:
            log.info('#### authenticated!!!!')
            return {'token': token}
        else:
            return 401
        return {}
    
    @view_config(route_name=Route.VERIFY_TOKEN,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def verify_token(self):
        """ This method is called from **/engine/api/verify_token**.
        """
        usr = self.request.params['user']
        pwd = self.request.params['pwd']
        log.info('usr: %s' % usr)
        log.info('pwd: %s' % pwd)
        user = self.authentication.access_app(usr, self.authentication._hash(pwd), Auth.USERS)
        log.info('user: %s' % user)
        token = self.authentication.get_token(1, user)
        log.info('token: %s' % token)
        response = self.authentication.verify_token(1, user, token)
        return {'response': response}

    @view_config(route_name=Route.CHECKOUT,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def checkout(self):
        """ This method is called from **/engine/api/checkout**.
        """
        data = self.request.json_body
        return {}
