
from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
import requests
from collections import namedtuple
from aaa_manager.emails import Emails
from aaa_manager.api.emails import EmailsRestView


@given('I have correct query string parameters username and email')
def step_impl(context):
    context.username = 'teste'
    context.email = 'email@teste.com'

@when('I call create email RESP API service')
def step_impl(context):
    pass

@then('I receive expected success response from email association')
def step_impl(context):
    payload = {
            'username': context.username,
            'email': context.email,
            }
    context.request = context.request(context.settings, params=payload)
    ret = {}
    with patch.object(Emails, 'create', 
            return_value=ret) as mck_create:
        emails = EmailsRestView(context.request)
        result = emails.create()
        assert mck_create.called
        assert result['success'] ==  'Email association successfully created.'

