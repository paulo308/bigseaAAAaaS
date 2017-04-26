
from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
from aaa_manager.emails import Emails
from aaa_manager.basedb import BaseDB

#Scenario: Create email
@given('I have correct username and email')
def step_impl(context):
    context.username = 'teste'
    context.email = 'email@teste.com'
    context.email_info = {
            'email': context.email
            }

@when('I create email')
def step_impl(context):
    pass

@then('I create email successfully')
def step_impl(context):
    with patch.object(BaseDB, 'insert',
            return_value=True) as mck_insert:
        emails = Emails()
        emails.create(
                context.username, 
                context.email_info)
        assert mck_insert.called
    
