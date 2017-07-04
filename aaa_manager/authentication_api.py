"""
This file contains the AAA manager REST interface. The API allows to manage 
authentication, authorisation and accounting information.
"""
import logging

from aaa_manager import Route
from aaa_manager.authentication import AuthenticationManager, Auth
from pyramid.view import view_config

LOG = logging.getLogger(__name__)


class AuthenticationRestView:
    """
    Implements the main REST API.
    """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']
        self.authentication = AuthenticationManager()

    @view_config(route_name=Route.CHECKIN,
                 request_method='POST',
                 renderer='json')
    def checkin(self):
        """ 
        This method is called from **/engine/api/checkin_data**.
        This method is used to authentication user to access the application.

        Arguments:
            user (str): the username;
            pwd (str): the user password.

        Returns:
            success (bool): True if sucessfully authenticated and False
            otherwise;
            cancelled (bool): True if operation is cancelled by the user and
            False otherwise;
            user_info (dict): contains information about the user, such as
            the authentication token and username;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            usr = self.request.params['user']
            pwd = self.request.params['pwd']
            # TODO: aap_id = 2 is hardcoded
            user = self.authentication.access_app(
                    2, 
                    usr, 
                    pwd, 
                    Auth.USERS)

            if user is not None:
                token = self.authentication.generate_token(user)
                response = self.authentication.insert_token(2, user, token)
                LOG.info('Successfully authenticated.')
                return {
                        'success': True, 
                        'cancelled': False, 
                        'user_info': {'user_token': token, 'user': user}, 
                        'error': ''
                        }
            else:
                LOG.info('User not authenticated.')
                return {
                        'success': False, 
                        'cancelled': False, 
                        'user_info': None, 
                        'error': 'Invalid username or password.'
                        }
            return {}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
        LOG.info(msg)
        return {'error': msg}

    @view_config(route_name=Route.CHECKOUT,
                 request_method='POST',
                 renderer='json')
    def checkout(self):
        """ 
        This method is called from **/engine/api/checkout_data**.
        This method is used to logout. It revocates current user token and
        logs the operation for accounting purposes. 

        Args:
            token (str): hexadecimal representation of user token.
        """
        msg = ''
        try:
            token = self.request.params['token']
            result = self.authentication.remove_token(token)
            if result is not None:
                LOG.info('Successfully checkout.')
                return {
                        'success': True, 
                        'cancelled': False, 
                        'user_info': {'user_token': token}, 
                        'error': ''
                        }
            else:
                LOG.info('User not checkin.')
                return {
                        'success': False, 
                        'cancelled': False, 
                        'user_info': None, 
                        'error': 'Invalid token.'
                        }
            return {}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
        LOG.info(msg)
        return {'error': msg}

    @view_config(route_name=Route.VERIFY_TOKEN,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def verify_token(self):
        """ 
        This method is called from **/engine/api/verify_token**.
        Verify the validity of user token. 

        Args:
            token (str): hexadecimal representation of user token.

        Returns:
            response (str): username if token is valid and 'invalid token'
            otherwise. 
        """
        msg = ''
        try:
            token = self.request.params['token']
            LOG.info('#### Input token: %s' % token)
            response = self.authentication.verify_token(2, token)
            return {'response': response}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
        LOG.info(msg)
        return {'error': msg}
    
    @view_config(route_name=Route.READ_USER_INFO,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def read_user_info(self):
        """ 
        This method is called from **/engine/api/read_user_info**.
        Verify the validity of user token. 

        Args:
            token (str): hexadecimal representation of user token.

        Returns:
            response (str): username if token is valid and 'invalid token'
            otherwise. 
        """
        msg = ''
        try:
            token = self.request.params['token']
            LOG.info('#### Input token: %s' % token)
            response = self.authentication.read_user_info(2, token)
            return {'response': response,
                    'success': 'User info read successfully.'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
        LOG.info(msg)
        return {'error': msg}

    @view_config(route_name=Route.SIGNUP,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def signup(self):
        """ 
        This method is called from **/engine/api/signup**.
        Method used to register new user into the system.

        Args:
            user (str): username;
            pwd (str): user password;
            fname (str): user first name;
            lname (str): user last name;
            email (str): user email address. 
        """
        msg = ''
        try:
            LOG.info('Awaits filling forms...')

            usr = self.request.params['user']
            pwd = self.request.params['pwd']
            fname = self.request.params['fname']
            lname = self.request.params['lname']
            email = self.request.params['email']

            user_info = {
                    'username': usr, 
                    'password': pwd, 
                    'fname': fname, 
                    'lname': lname,
                    'email': email
                    }
            # app_id = 2 is hardcoded for now.
            # TODO: remove hardcoded data
            result = self.authentication.insert_user(2, user_info)

            if result[0] is not None and result[1] == '':
                LOG.info('User successfully registered.')
                return {'success': 'User signed up with success.'}
            if result[0] is None and result[1] != '':
                LOG.info(result[1])
                return {'error': result[1]}
            else:
                LOG.info('Username already exists.')
                return {'error':\
                        'Username already exists. Please choose a different one.'
                }
            return {}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
        LOG.info(msg)
        return {'error': msg}

    
    @view_config(route_name=Route.UPDATE_USER,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def update_user(self):
        """ 
        This method is called from **/engine/api/update_user**.
        Method used to update user information on the system.

        Args:
            user (str): username;
            pwd (str): user password;
            fname (str): user first name;
            lname (str): user last name;
            email (str): user email address. 
        """
        msg = ''
        try:
            usr = self.request.params['user']
            fname = self.request.params['fname']
            lname = self.request.params['lname']
            email = self.request.params['email']
            token = self.request.params['token']
                
            LOG.info('#### usr: %s' % usr)
            LOG.info('#### fname: %s' % fname)
            LOG.info('#### lname: %s' % lname)
            LOG.info('#### email: %s' % email)
            LOG.info('#### token: %s' % token)

            user_info = {
                    'username': usr, 
                    'fname': fname, 
                    'lname': lname,
                    'email': email, 
                    'token': token
                    }
            result = self.authentication.update_user(2, user_info)
            LOG.info('#### result: %s' % result)
            if result > 0:
                msg = 'User information updated successfully.'
                LOG.info(msg)
                return {'success': msg}
            else:
                msg = 'Username does not exist.'
                LOG.info(msg)
                return {'error': msg}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
        LOG.info(msg)
        return {'error': msg}
    
    @view_config(route_name=Route.CHANGE_PASSWORD,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def change_password(self):
        """ 
        This method is called from **/engine/api/update_user**.
        Method used to update user information on the system.

        Args:
            user (str): username;
            oldpwd (str): old password;
            newpwd (str): new password;
            token (str): token.
        """

        msg = ''
        try:
            usr = self.request.params['user']
            oldpwd = self.request.params['oldpwd']
            newpwd = self.request.params['newpwd']
            token = self.request.params['token']

            LOG.info('#### usr: %s' % usr)
            LOG.info('#### oldpwd: %s' % oldpwd)
            LOG.info('#### newpwd: %s' % newpwd)
            LOG.info('#### token: %s' % token)

            user_info = {
                    'username': usr, 
                    'oldpwd': oldpwd, 
                    'newpwd':newpwd, 
                    'token': token
                    }
            result = self.authentication.change_password(2, user_info)
            LOG.info('#### result: %s' % result)
            if result > 0:
                msg = 'Password updated successfully.'
                LOG.info(msg)
                return {'success': msg}
            else:
                msg = 'Username does not exist.'
                LOG.info(msg)
                return {'error': msg}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
        LOG.info(msg)
        return {'error': msg}

    @view_config(route_name=Route.DELETE_USER,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def delete_user(self):
        """
        This method is called from **/engine/api/update_user
        Method used to delete user information from application.

        Args:
            username (str): username;
            pwd (str): user password;
            fname (str): user first name;
            lname (str): user last name;
            email (str): user email address. 
        """

        msg = ''
        try:
            usr = self.request.params['user']
            token = self.request.params['token']
            user_info = {
                    'username': usr, 
                    'token': token, 

                    }

            result = self.authentication.delete_user(2, user_info)
            LOG.info('#### result: %s' % result)
            if result > 0:
                msg = 'User deleted with success.'
                LOG.info(msg)
                return {'success': msg}
            else:
                msg = 'User does not exist.'
                LOG.info(msg)
                return {'error': msg}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
        LOG.info(msg)
        return {'error': msg}


    @view_config(route_name=Route.EMAIL_CONFIRMATION,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def email_confirmation(self):
        """
        This method is called from **/engine/api/email_confirmation
        Method used to confirm that the user possess given email address.

        Args:
            username (str): username;
            email_token (str): unique email token.
            email (str): user email.
        """

        msg = ''
        try:
            username = self.request.params['username']
            email_token = self.request.params['token']
            email = self.request.params['email']
            result = self.authentication.email_confirmation(username, email, email_token)
            if result:
                msg = 'User email confirmed with success.'
                LOG.info(msg)
                return {'success': msg}
            else:
                msg = 'User email was not confirmed.'
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
        LOG.info(msg)
        return {'error': msg}

    @view_config(route_name=Route.SEND_EMAIL_TOKEN,
                 request_method='POST',
                 accept='application/json',
                 renderer='json')
    def send_email_token(self):
        """
        This method is called from **/engine/api/send_email_token
        Method used to send email with token.

        Args:
            username (str): username;
            email (str): user email.
        """

        msg = ''
        try:
            username = self.request.params['username']
            email = self.request.params['email']
            result = self.authentication.send_email_token(username, email)
            LOG.info('#### result: %s' % result)
            if result:
                msg = 'Email sent with success.'
                LOG.info(msg)
                return {'success': msg}
            else:
                msg = 'Email was not sent.'
                LOG.info(msg)
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
        LOG.info(msg)
        return {'error': msg}

