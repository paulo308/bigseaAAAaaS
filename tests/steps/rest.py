"""
REST API unit tests.
"""

from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
import requests
from collections import namedtuple
from aaa_manager.rest import RestView 
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
    settings = namedtuple('settings', 'settings')
    settings = settings({'data': {}})
    params = payload
    request = namedtuple('request', 'registry params')
    request = request(settings, params)
    ret = [{}], ''
    with patch.object(AuthenticationManager, 'insert_user',
            return_value=ret) as mck_insert:
        rv = RestView(request)
        result = rv.signup()
        assert result['success'] == 'User signed up with success.'
        assert mck_insert.called
    ret = None, ''
    with patch.object(AuthenticationManager, 'insert_user',
            return_value=ret) as mck_insert:
        rv = RestView(request)
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
    settings = namedtuple('settings', 'settings')
    settings = settings({'data': {}})
    params = payload
    request = namedtuple('request', 'registry params')
    request = request(settings, params)
    ret = None, 'invalid user information'
    with patch.object(AuthenticationManager, 'insert_user',
            return_value=ret) as mck_insert:
        rv = RestView(request)
        result = rv.signup()
        assert result['error'] == 'invalid user information'
        assert mck_insert.called
    ret = None, 'invalid user information'
    with patch.object(AuthenticationManager, 'insert_user',
            return_value=ret) as mck_insert:
        rv = RestView(request)
        result = rv.signup()
        assert result['error'] == 'invalid user information'
        assert mck_insert.called

#Scenario: Checkin
@given('I have user credential')
def step_impl(context):
    assert False

@when('I checkin')
def step_impl(context):
    assert False

@then('I checkin successully')
def step_impl(context):
    assert False

#Scenario: Checkin
@given('I have wrong user credential')
def step_impl(context):
    assert False

@then('I receive expected checkin error message')
def step_impl(context):
    assert False

#Scenario: Checkout
@given('I have correct user token')
def step_impl(context):
    assert False

@when('I checkout')
def step_impl(context):
    assert False

@then('I checkout successfully')
def step_impl(context):
    assert False

#Scenario: Checkout
@given('I have wrong user token')
def step_impl(context):
    assert False

@then('I receive expected checkout error message')
def step_impl(context):
    assert False

#Scenario: Update user
@given('I have new user information and a valid token')
def step_impl(context):
    assert False

@when('I update user using REST API')
def step_impl(context):
    assert False

@then('I update user successfully using REST API')
def step_impl(context):
    assert False

#Scenario: Update user
@given('I have wrong new user information or an invalid token')
def step_impl(context):
    assert False

@then('I receive corresponding update user error message')
def step_impl(context):
    assert False

#Scenario: Delete user
@given('I have wrong user information and a valid token')
def step_impl(context):
    assert False

@when('I delete user using REST API')
def step_impl(context):
    assert False

@then('I receive corresponding delete user error message')
def step_impl(context):
    assert False

#Scenario: Delete user
@given('I have correct user information and a valid token')
def step_impl(context):
    assert False

@then('I delete user successfully using REST API')
def step_impl(context):
    assert False
