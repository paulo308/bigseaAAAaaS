from pyramid.config import Configurator
from aaa_manager.route import Route

import logging

LOG = logging.getLogger(__name__)

def main(global_config, **settings):
    """
    Function called by gunicorn to map routes.
    """
    LOG.info("Setting AAA module routes...")
    settings['data'] = []
    config = Configurator(settings=settings)
    config.add_static_view(Route.STATIC_ASSETS, 'pages/templates/static')

    # jinja2 template
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('pages/templates')

    # web routes
    config.add_route(Route.HOME, '/')
    config.add_route(Route.WEB, '/web')
    config.add_route(Route.WEB_CHECKIN, '/web/checkin')
    config.add_route(Route.WEB_CHECKOUT, '/web/checkout')
    config.add_route(Route.WEB_SIGNUP, '/web/signup')
    config.add_route(Route.WEB_MANAGE_AUTH, 'web/manage_info_auth')
    config.add_route(Route.WEB_MANAGE_USER, 'web/manage_info_user')
    config.add_route(Route.WEB_MANAGE_ADMIN, 'web/manage_info_admin')
    config.add_route(Route.WEB_EMAIL_CONFIRMATION, 'web/email_confirmation')
    config.add_route(Route.WEB_SIGNIN_OPTIONS, 'web/signin_options')

    # json routes
    config.add_route(Route.GET_CHECKIN, '/json/checkin')
    config.add_route(Route.GET_CHECKOUT, '/json/checkout')
    config.add_route(Route.GET_SIGNUP, '/json/signup')
    config.add_route(Route.GET_VERIFY_TOKEN, '/json/verify_token')
    config.add_route(Route.GET_READ_USER_INFO, '/json/read_user_info')
    config.add_route(Route.GET_UPDATE_USER, '/json/update')
    config.add_route(Route.GET_CHANGE_PASSWORD, '/json/change_password')
    config.add_route(Route.GET_FORGOT_PASSWORD, '/json/forgot_password')
    config.add_route(Route.GET_DELETE_USER, '/json/delete')
    config.add_route(Route.GET_EMAIL_CONFIRMATION, '/json/email_confirmation')
    config.add_route(Route.GET_SEND_EMAIL_TOKEN, '/json/send_email_token')
    config.add_route(Route.GET_CREATE_AUTHORISATION, '/json/create_authorisation')
    config.add_route(Route.GET_USE_RESOURCE, '/json/use_resource')
    config.add_route(Route.GET_CREATE_EMAIL, '/json/create_email')
    config.add_route(Route.GET_READ_EMAILS, '/json/read_emails')
    config.add_route(Route.GET_DELETE_EMAIL, '/json/delete_email')
    config.add_route(Route.GET_CREATE_FAVORITE, '/json/create_favorite')
    config.add_route(Route.GET_READ_FAVORITE, '/json/read_favorite')
    config.add_route(Route.GET_READ_FAVORITES, '/json/read_favorites')
    config.add_route(Route.GET_DELETE_FAVORITE, '/json/delete_favorite')
    config.add_route(Route.GET_READ_ACCOUNTING, '/json/read_accounting')

    # rest api routes
    config.add_route(Route.CHECKIN, '/engine/api/checkin_data')
    config.add_route(Route.CHECKOUT, '/engine/api/checkout_data')
    config.add_route(Route.SIGNUP, '/engine/api/signup_data')
    config.add_route(Route.VERIFY_TOKEN, '/engine/api/verify_token')
    config.add_route(Route.READ_USER_INFO, '/engine/api/read_user_info')
    config.add_route(Route.UPDATE_USER, '/engine/api/update_user')
    config.add_route(Route.CHANGE_PASSWORD, '/engine/api/change_password')
    config.add_route(Route.FORGOT_PASSWORD, '/engine/api/forgot_password')
    config.add_route(Route.DELETE_USER, '/engine/api/delete_user')
    config.add_route(Route.EMAIL_CONFIRMATION, '/engine/api/email_confirmation')
    config.add_route(Route.SEND_EMAIL_TOKEN, '/engine/api/send_email_token')
    config.add_route(Route.CREATE_AUTHORISATION, '/engine/api/create_authorisation')
    config.add_route(Route.READ_AUTHORISATION, '/engine/api/read_authorisation')
    config.add_route(Route.READ_AUTHORISATIONS, '/engine/api/read_authorisations')
    config.add_route(Route.UPDATE_AUTHORISATION, '/engine/api/update_authorisation')
    config.add_route(Route.DELETE_AUTHORISATION, '/engine/api/delete_authorisation')
    config.add_route(Route.USE_RESOURCE, '/engine/api/use_resource')
    config.add_route(Route.CREATE_EMAIL, '/engine/api/create_email')
    config.add_route(Route.READ_EMAILS, '/engine/api/read_emails')
    config.add_route(Route.DELETE_EMAIL, '/engine/api/delete_email')
    config.add_route(Route.CREATE_FAVORITE, '/engine/api/create_favorite')
    config.add_route(Route.READ_FAVORITE, '/engine/api/read_favorite')
    config.add_route(Route.READ_FAVORITES, '/engine/api/read_favorites')
    config.add_route(Route.DELETE_FAVORITE, '/engine/api/delete_favorite')
    config.add_route(Route.READ_ACCOUNTING, '/engine/api/read_accounting')

    LOG.info("AAA module initiated.")
    # Scan and load classes with configuration decoration (@view_config)
    config.scan()
    return config.make_wsgi_app()
