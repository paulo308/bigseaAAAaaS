"""
REST API unit tests.
"""

from behave import given, when, then

#Scenario: Signup
@given('I have correct user information')
def step_impl(context):
    assert False

@when('I signup')
def step_impl(context):
    assert False

@then('I signup successfully')
def step_impl(context):
    assert False

#Scenario: Signup
@given('I have wrong user information')
def step_impl(context):
    assert False

@then('I receive expected signup error message')
def step_impl(context):
    assert False

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
