class Route:
    """ Routes names """
    # WEB routes
    HOME = "home"
    WEB = "home_web"
    WEB_CHECKIN = "checkin"
    WEB_CHECKOUT = "checkout"
    WEB_SIGNUP = "signup"
    WEB_SETTINGS = "settings"
    WEB_MANAGE_AUTH = "manage_info_auth"
    WEB_MANAGE_USER = "manage_info_user"
    WEB_MANAGE_ADMIN = "manage_info_admin"
    # REST API routes
    GET_CHECKIN = "checkin_data"
    GET_CHECKOUT = "checkout_data"
    GET_SIGNUP = "signup_data"
    GET_UPDATE_USER = "update_user_data"
    GET_DELETE_USER = "delete_user_data"
    # REST API routes
    CHECKIN = "checkin_state"
    CHECKOUT = "checkout_state"
    SIGNUP = "signup_state"
    VERIFY_TOKEN = "verify_token"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    # json routes
    CHECKIN_STATE = "get_checkin_state"
    CHECKOUT_STATE = "get_checkout_state"
    SIGNUP_STATE = "get_signup_state"
    # static assets routes
    STATIC_ASSETS = "static"
