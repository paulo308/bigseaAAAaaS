"""
Authentication unit tests.
"""

from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
from aaa_manager.authentication import AuthenticationManager
from aaa_manager.basedb import BaseDB
                
@given('I have user information and application identification')
def step_impl(context):
    context.user_info = {
            'username': 'unitteste', 
            'password': 'unitpwd', 
            'fname': 'unitfname', 
            'lname': 'unitlname',
            'email': 'unit@test.com'
            }
    context.app_id = 1

@when('I user is not repeated')
def step_impl(context):
    pass
    

@then('User is successfully created')
def step_impl(context):
    with patch.object(AuthenticationManager, '_is_user_unique',
            return_value=True) as mck_unique:
        with patch.object(BaseDB, 'insert',
                return_value=None) as mck_insert:
            authentication = AuthenticationManager()
            result = authentication.insert_user(context.app_id, 
                    context.user_info)
            assert mck_insert.called
            assert mck_unique.called
                
@when('I user is repeated')
def step_impl(context):
    pass

@then("User is not created and user string is returned")
def step_impl(context):
    with patch.object(AuthenticationManager, '_is_user_unique',
            return_value=False) as mck_unique:
        with patch.object(BaseDB, 'insert',
                return_value=None) as mck_insert:
            authentication = AuthenticationManager()
            result = authentication.insert_user(context.app_id, 
                    context.user_info)
            assert not mck_insert.called
            assert mck_unique.called
            print(result)
            assert len(result) == 2
            assert result[0] == None
            assert result[1] == 'users'

@when('I user is admin')
def step_impl(context):
    pass

@then("User is not created and admin string is returned")
def step_impl(context):
    context.user_info['username'] = 'admin'
    with patch.object(AuthenticationManager, '_is_user_unique',
            return_value=False) as mck_unique:
        with patch.object(BaseDB, 'insert',
                return_value=None) as mck_insert:
            authentication = AuthenticationManager()
            result = authentication.insert_user(context.app_id, 
                    context.user_info)
            assert not mck_insert.called
            assert not mck_unique.called
            print(result)
            assert len(result) == 2
            assert result[0] == None
            assert result[1] == 'admin'

@given('I have username and password')
def step_impl(context):
    context.username = 'teste'
    context.password = 'pwd'

@when('I access application')
def step_impl(context):
    context.info = {'username': 'teste', 'password': 'pwd'}
    ret = [{'auth': [context.info]}]
    with patch.object(BaseDB, 'get', 
        return_value=ret) as mck_get:
            authentication = AuthenticationManager()
            context.result = authentication.access_app(1,
                context.username, context.password)
            assert mck_get.called

@then('I get user information')
def step_impl(context):
    assert context.result == context.info
                
@given('I have valid application ID and user information')
def step_impl(context):
    context.app_id = 1
    context.user_info = {'username': 'teste', 'password': 'pwd'}

@when('I consult token')
def step_impl(context):
    context.token = 'abababab'
    ret = [{
            'data': [{
                'app_id': context.app_id, 
                'user': context.user_info
            }],
            'token': context.token
        }]
    with patch.object(BaseDB, 'get_all', return_value=ret) as mck_get:
        authentication = AuthenticationManager()
        context.result = authentication.get_token(context.app_id, context.user_info)
        

@then('I get valid token')
def step_impl(context):
    assert context.result == context.token
                
@given('I have valid application ID and token')
def step_impl(context):
    context.app_id = 1
    context.username = 'teste'
    context.user_info = {'username': context.username, 'password': 'pwd'}
    context.token = 'ababab'
    ret = [{
            'data': [{
                'app_id': context.app_id, 
                'status': 'valid',
                'user': context.user_info
            }],
            'token': context.token
        }]
    with patch.object(BaseDB, 'get', return_value=ret) as mck_get:
        authentication = AuthenticationManager()
        context.result = authentication.verify_token(context.app_id,
                context.token)
        assert mck_get.called
        
@when('I verify token')
def step_impl(context):
    pass

@then('I get corresponding username')
def step_impl(context):
    assert context.result == context.username
                
@given('I have valid application ID, user information and token')
def step_impl(context):
    context.app_id = 1
    context.username = 'teste'
    context.user_info = {'username': context.username, 'password': 'pwd'}
    context.token = 'ababab'
    context.data = {
            'app_id': context.app_id, 
            'status': 'valid',
            'user': context.user_info
            }
    with patch.object(BaseDB, 'update') as mck_update:
        with patch.object(BaseDB, 'insert') as mck_insert:
            authentication = AuthenticationManager()
            context.result = authentication.insert_token(context.app_id,
                    context.user_info,
                    context.token)
            assert mck_update.called
            assert mck_update.called_with('Token', 'token', context.token,
            'data', context.data)
            assert mck_insert.called

@when('I insert token')
def step_impl(context):
    pass

@then('I get database response')
def step_impl(context):
    assert context.result is not None
