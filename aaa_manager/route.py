class Route:
    """ Routes names """
    # WEB routes
    HOME = "home"
    WEB = "home_web"
    WEB_CHECKIN = "checkin"
    WEB_CHECKOUT = "checkout"
    WEB_SIGNUP = "signup"
    WEB_SETTINGS = "settings"
    # REST API routes
    GET_CHECKIN = "checkin_data"
    GET_CHECKOUT = "checkout_data"
    GET_SIGNUP = "signup_data"
    GET_UPDATE_USER = "update_user_data"
    GET_DELETE_USER = "delete_user_data"
    GET_CREATE_AUTHORISATION = "create_authorisation_data"
    # REST API routes
    CHECKIN = "checkin_state"
    CHECKOUT = "checkout_state"
    SIGNUP = "signup_state"
    VERIFY_TOKEN = "verify_token"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    CREATE_AUTHORISATION = "create_authorisation"
    # json routes
    CHECKIN_STATE = "get_checkin_state"
    CHECKOUT_STATE = "get_checkout_state"
    SIGNUP_STATE = "get_signup_state"
    # static assets routes
    STATIC_ASSETS = "static"
