from pyramid.config import Configurator
from aaa_manager.route import Route


def main(global_config, **settings):
    """
    Function called by gunicorn to map routes.
    """
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

    # json routes
    config.add_route(Route.GET_CHECKIN, '/json/checkin')
    config.add_route(Route.GET_CHECKOUT, '/json/checkout')
    config.add_route(Route.GET_SIGNUP, '/json/signup')
    config.add_route(Route.GET_UPDATE_USER, '/json/update')
    config.add_route(Route.GET_CHANGE_PASSWORD, '/json/change_password')
    config.add_route(Route.GET_DELETE_USER, '/json/delete')
    config.add_route(Route.GET_EMAIL_CONFIRMATION, '/json/email_confirmation')
    config.add_route(Route.GET_CREATE_AUTHORISATION, '/json/create_authorisation')

    # rest api routes
    config.add_route(Route.CHECKIN, '/engine/api/checkin_data')
    config.add_route(Route.CHECKOUT, '/engine/api/checkout_data')
    config.add_route(Route.SIGNUP, '/engine/api/signup_data')
    config.add_route(Route.VERIFY_TOKEN, '/engine/api/verify_token')
    config.add_route(Route.UPDATE_USER, '/engine/api/update_user')
    config.add_route(Route.CHANGE_PASSWORD, '/engine/api/change_password')
    config.add_route(Route.DELETE_USER, '/engine/api/delete_user')
    config.add_route(Route.EMAIL_CONFIRMATION, '/engine/api/email_confirmation')
    config.add_route(Route.CREATE_AUTHORISATION, '/engine/api/create_authorisation')

    # Scan and load classes with configuration decoration (@view_config)
    config.scan()
    return config.make_wsgi_app()
