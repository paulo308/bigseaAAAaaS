from aaa_manager.route import Route
from pyramid.view import view_config
from aaa_manager.authentication import AuthenticationManager
import logging
import json
import jsonschema

LOG = logging.getLogger(__name__)

class WebView:
    """ 
    Implements the web interface view.
    """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self.authentication = AuthenticationManager()

    @view_config(route_name=Route.WEB,
                 renderer='home.jinja2')
    @view_config(route_name=Route.HOME,
                 renderer='home.jinja2')
    def home(self):
        """
        This method is called from **/** or **/web**.
        """
        return ''

    @view_config(route_name=Route.WEB_CHECKIN,
                 renderer='login.jinja2')
    def checkin(self):
        """
        This method is called from **/web/checkin**.
        """
        return ''

    @view_config(route_name=Route.WEB_SIGNUP,
                 renderer='signup.jinja2')
    def signup(self):
        """
        This method is called from **/web/signup**.
        """
        return ''

    @view_config(route_name=Route.WEB_MANAGE_AUTH,
                 renderer='manage_info_auth.jinja2')
    def manage_info_auth(self):
        """
        This method is called from **/web/manage_info_auth**.
        """
        return ''

    @view_config(route_name=Route.WEB_MANAGE_USER,
                 renderer='manage_info_user.jinja2')
    def manage_info_user(self):
        """
        This method is called from **/web/manage_info_user**.
        """
        return ''

    @view_config(route_name=Route.WEB_MANAGE_ADMIN,
                 renderer='manage_info_admin.jinja2')
    def manage_info_admin(self):
        """
        This method is called from **/web/manage_info_admin**.
        """
        return ''
    
    @view_config(route_name=Route.WEB_SIGNIN_OPTIONS,
                 renderer='signin_options.jinja2')
    def signin_options(self):
        """
        This method is called from **/web/singin_options**.
        """
        return ''
    
    @view_config(route_name=Route.WEB_EMAIL_CONFIRMATION,
                 renderer='email_confirmation.jinja2')
    def email_confirmation(self):
        """
        This method is called from **/web/email_confirmation**.
        """
        return ''
