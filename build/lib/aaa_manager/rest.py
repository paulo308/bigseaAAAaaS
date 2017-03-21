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
                 renderer='json')
    def checkin(self):
        """ This method is called from **/engine/api/checkin**.
        """
        usr = self.request.params['user']
        pwd = self.request.params['pwd']
        user = self.authentication.access_app(2, usr, self.authentication._hash(pwd), Auth.USERS)
        token = self.authentication.generate_token(user)
        response = self.authentication.insert_token(2, user, token)

        if user is not None:
            log.info('#### authenticated!')
            return {'success': True, 'cancelled': False, 'user_info': {'user_token': token, 'user': user}, 'error': ''}
        else:
            log.info('#### not authenticated!')
            return {'success': False, 'cancelled': False, 'user_info': None, 'error': 'Invalid username or password.'}
        return {}

    @view_config(route_name=Route.CHECKOUT,
                 request_method='POST',
                 renderer='json')
    def checkout(self):
        """ This method is called from **/engine/api/checkout**.
        """
        token = self.request.params['token']
        self.authentication.remove_token(token)
        return {}

    @view_config(route_name=Route.VERIFY_TOKEN,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def verify_token(self):
        """ This method is called from **/engine/api/verify_token**.
        """
        token = self.request.params['token']
        response = self.authentication.verify_token(2, token)
        return {'response': response}

    @view_config(route_name=Route.SIGNUP,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def signup(self):
        """ This method is called from **/engine/api/signup**.
        """

        log.info('#### awaits filling forms...')
        #needs to collect info from forms, verify them, and input in database

        usr = self.request.params['user']
        pwd = self.request.params['pwd']
        fname = self.request.params['fname']
        lname = self.request.params['lname']
        email = self.request.params['email']

        log.info('usr: %s' % usr)
        log.info('pwd: %s' % pwd)
        log.info('fname: %s' % fname)
        log.info('lname: %s' % lname)
        log.info('email: %s' % email)

        user_info = {'username': usr, 'password': pwd, 'fname': fname, 'lname': lname}
	#user = insert_user(1, auth_info)
        result = self.authentication.insert_user(2, user_info)

        log.info('#### result: %s, %s' % result)
        if result[0] is not None:
            log.info('User registered!!!')
            return {'success': 'User signed up with success!'}
        else:
            log.info('Username already exists...')
            return {'error': 'Username already exists. Please choose a different one.'}
        return {}
