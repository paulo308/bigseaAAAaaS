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
