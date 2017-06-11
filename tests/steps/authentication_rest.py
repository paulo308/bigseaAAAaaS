"""
REST API unit tests.
"""

from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
import requests
from collections import namedtuple
from aaa_manager.api.authentication import AuthenticationRestView 
from aaa_manager.authentication import AuthenticationManager 


#Scenario: Signup
@given('I have correct user information')
def step_impl(context):
    context.user_info = {
            'username': 'teste',
            'password': '@bCd3fgh',
            'fname' : 'teste',
            'lname': 'teste',
            'email': 'teste@mail.com'
            }

@when('I signup')
def step_impl(context):
    pass

@then('I signup successfully')
def step_impl(context):
    payload = {
            'user': context.user_info['username'],
            'pwd': context.user_info['password'],
            'fname': context.user_info['fname'],
            'lname': context.user_info['lname'],
            'email': context.user_info['email']
            }
    context.request = context.request(context.settings, params=payload)
    ret = [{}], ''
    with patch.object(AuthenticationManager, 'insert_user',
            return_value=ret) as mck_insert:
        rv = AuthenticationRestView(context.request)
        result = rv.signup()
        assert result['success'] == 'User signed up with success.'
        assert mck_insert.called
    ret = None, ''
    with patch.object(AuthenticationManager, 'insert_user',
            return_value=ret) as mck_insert:
        rv = AuthenticationRestView(context.request)
        result = rv.signup()
        assert result['error'] == 'Username already exists. Please choose a different one.'
        assert mck_insert.called


#Scenario: Signup
@given('I have wrong user information')
def step_impl(context):
    context.user_info = {
            'username': 'teste',
            'password': '@bCd3fgh',
            'fname' : 'teste',
            'lname': 'teste',
            'email': 'teste' 
            }

@then('I receive expected signup error message')
def step_impl(context):
    payload = {
            'user': context.user_info['username'],
            'pwd': context.user_info['password'],
            'fname': context.user_info['fname'],
            'lname': context.user_info['lname'],
            'email': context.user_info['email']
            }
    context.request = context.request(context.settings, params=payload)
    ret = None, 'invalid user information'
    with patch.object(AuthenticationManager, 'insert_user',
            return_value=ret) as mck_insert:
        rv = AuthenticationRestView(context.request)
        result = rv.signup()
        assert result['error'] == 'invalid user information'
        assert mck_insert.called
    ret = None, 'invalid user information'
    with patch.object(AuthenticationManager, 'insert_user',
            return_value=ret) as mck_insert:
        rv = AuthenticationRestView(context.request)
        result = rv.signup()
        assert result['error'] == 'invalid user information'
        assert mck_insert.called

#Scenario: Checkin
@given('I have user credential')
def step_impl(context):
    context.user_info = {
            'username': 'teste',
            'password': '@bCd3fgh'
            }

@when('I checkin')
def step_impl(context):
    pass

@then('I checkin successully')
def step_impl(context):
    payload = {
            'user': context.user_info['username'],
            'pwd': context.user_info['password']
            }
    context.request = context.request(context.settings, params=payload)
    ret = {}
    with patch.object(AuthenticationManager, 'access_app',
            return_value=ret) as mck_access:
        with patch.object(AuthenticationManager, 'generate_token',
                return_value=ret) as mck_gen:
            with patch.object(AuthenticationManager, 'insert_token',
                    return_value=ret) as mck_insert:
                rv = AuthenticationRestView(context.request)
                result = rv.checkin()
                assert result['success']
                assert mck_access.called
                assert mck_gen.called
                assert mck_insert.called

#Scenario: Checkin
@given('I have wrong user credential')
def step_impl(context):
    context.user_info = {
            'username': 'teste',
            'password': '@bCd3fgh'
            }

@then('I receive expected checkin error message')
def step_impl(context):
    payload = {
            'user': context.user_info['username'],
            'pwd': context.user_info['password']
            }
    context.request = context.request(context.settings, params=payload)
    ret = None
    with patch.object(AuthenticationManager, 'access_app',
            return_value=ret) as mck_access:
        with patch.object(AuthenticationManager, 'generate_token',
                return_value=ret) as mck_gen:
            with patch.object(AuthenticationManager, 'insert_token',
                    return_value=ret) as mck_insert:
                rv = AuthenticationRestView(context.request)
                result = rv.checkin()
                assert not result['success']
                assert mck_access.called
                assert not mck_gen.called
                assert not mck_insert.called

#Scenario: Checkout
@given('I have correct user token')
def step_impl(context):
    context.token = 'abababa'

@when('I checkout')
def step_impl(context):
    pass

@then('I checkout successfully')
def step_impl(context):
    payload = {
            'token': context.token
            }
    context.request = context.request(context.settings, params=payload)
    ret = None
    with patch.object(AuthenticationManager, 'remove_token',
            return_value=ret) as mck_remove:
        rv = AuthenticationRestView(context.request)
        result = rv.checkout()
        assert mck_remove.called_with('2', context.token)

#Scenario: Checkout
@given('I have wrong user token')
def step_impl(context):
    assert True


@then('I receive expected checkout error message')
def step_impl(context):
    assert True

#Scenario: Update user
@given('I have new user information and a valid token')
def step_impl(context):
    context.user_info = {
            'token': 'abababab',
            'username': 'teste',
            'fname' : 'teste',
            'lname': 'teste',
            'email': 'teste@mail.com'
            }


@when('I update user using REST API')
def step_impl(context):
    pass

@then('I update user successfully using REST API')
def step_impl(context):
    payload = {
            'token': context.user_info['token'],
            'user': context.user_info['username'],
            'fname': context.user_info['fname'],
            'lname': context.user_info['lname'],
            'email': context.user_info['email']
            }
    context.request = context.request(context.settings, params=payload)
    ret = 1    # corresponds to 1 updated item 
    with patch.object(AuthenticationManager, 'update_user',
            return_value=ret) as mck_update:
        rv = AuthenticationRestView(context.request)
        result = rv.update_user()
        assert mck_update.called
        assert result['success'] == 'User information updated successfully.'

#Scenario: Update user
@given('I have wrong new user information or an invalid token')
def step_impl(context):
    context.user_info = {
            'token': 'abababab',
            'username': 'teste',
            'fname' : 'teste',
            'lname': 'teste',
            'email': 'teste@mail.com'
            }


@then('I receive corresponding update user error message')
def step_impl(context):
    payload = {
            'token': context.user_info['token'],
            'user': context.user_info['username'],
            'fname': context.user_info['fname'],
            'lname': context.user_info['lname'],
            'email': context.user_info['email']
            }
    context.request = context.request(context.settings, params=payload)
    ret = 0    # corresponds to 1 updated item 
    with patch.object(AuthenticationManager, 'update_user',
            return_value=ret) as mck_update:
        rv = AuthenticationRestView(context.request)
        result = rv.update_user()
        assert mck_update.called
        assert result['error'] == 'Username does not exist.'

#Scenario: Delete user
@given('I have wrong user information and a valid token')
def step_impl(context):
    context.user_info = {
            'username': 'teste',
            'token': 'abababa'
            }

@when('I delete user using REST API')
def step_impl(context):
    pass

@then('I receive corresponding delete user error message')
def step_impl(context):
    payload = {
            'user': context.user_info['username'],
            'token': context.user_info['token']
            }
    context.request = context.request(context.settings, params=payload)
    ret = 1    # corresponds to 1 updated item 
    with patch.object(AuthenticationManager, 'delete_user',
            return_value=ret) as mck_delete:
        rv = AuthenticationRestView(context.request)
        result = rv.delete_user()
        assert mck_delete.called
        assert result['success'] == 'User deleted with success.'

#Scenario: Delete user
@given('I have correct user information and a valid token')
def step_impl(context):
    context.user_info = {
            'username': 'teste',
            'token': 'abababa'
            }

@then('I delete user successfully using REST API')
def step_impl(context):
    payload = {
            'user': context.user_info['username'],
            'token': context.user_info['token']
            }
    context.request = context.request(context.settings, params=payload)
    ret = 0    # corresponds to 1 updated item 
    with patch.object(AuthenticationManager, 'delete_user',
            return_value=ret) as mck_delete:
        rv = AuthenticationRestView(context.request)
        result = rv.delete_user()
        assert mck_delete.called
        assert result['error'] == 'User does not exist.'

@given('I have valid username and email token')
def step_impl(context):
    context.user_info = {
            'username': 'teste',
            'email': 'eduardo.morais@gmail.com',
            'token' : 'ababab'
            }

@when('I call the email confirmation REST API')
def step_impl(context):
    pass

@then('I receive expected email confirmation message')
def step_impl(context):
    payload = {
            'username': context.user_info['username'],
            'email': context.user_info['email'],
            'token': context.user_info['token']
            }
    context.request = context.request(context.settings, params=payload)
    rv = AuthenticationRestView(context.request)
    result = rv.email_confirmation()
    
