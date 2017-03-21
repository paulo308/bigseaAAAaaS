from pyramid.config import Configurator
from aaa_manager.route import Route


def main(global_config, **settings):
    """Function called by gunicorn"""
    settings['data'] = []
    config = Configurator(settings=settings)
    # Static configuration
    config.add_static_view(Route.STATIC_ASSETS, 'pages/templates/static')
    # Add jinja2 as template
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('pages/templates')
    # Add web client routes
    config.add_route(Route.HOME, '/')
    config.add_route(Route.WEB, '/web')
    config.add_route(Route.WEB_CHECKIN, '/web/checkin')
    config.add_route(Route.WEB_CHECKOUT, '/web/checkout')
    config.add_route(Route.WEB_SIGNUP, '/web/signup')
    # Add JSON routes
    config.add_route(Route.GET_CHECKIN, '/json/checkin')
    config.add_route(Route.GET_CHECKOUT, '/json/checkout')
    config.add_route(Route.GET_SIGNUP, '/json/signup')
    # Add device REST API routes
    config.add_route(Route.CHECKIN, '/engine/api/checkin_data')
    config.add_route(Route.CHECKOUT, '/engine/api/checkout_data')
    config.add_route(Route.SIGNUP, '/engine/api/signup_data')
    config.add_route(Route.VERIFY_TOKEN, '/engine/api/verify_token')
    # Scan and load classes with configuration decoration (@view_config)
    config.scan()
    return config.make_wsgi_app()
