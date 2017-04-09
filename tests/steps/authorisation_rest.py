
from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
import requests
from collections import namedtuple
from aaa_manager.authorisation import Authorisation
from aaa_manager.authorisation_rest import AuthorisationRestView


@given('I have correct query string parameters username, resource name and rule')
def step_impl(context):
    context.username = 'teste'
    context.resource_name = 'rest service'
    context.rule = {
            'resource_name': context.resource_name,
            'resource_type': 'rest',
            'app_id': 2,
            'max_used': 100,
            'used': 0,
            'url': 'http://teste.com/service',
            'blob': 'jgyfhftf'
            }

@when('I call create rule RESP API service')
def step_impl(context):
    pass

@then('I receive expected success response')
def step_impl(context):
    payload = {
            'username': context.username,
            'resource_name': context.resource_name,
            'rule': context.rule
            }
    context.request = context.request(context.settings, params=payload)
    ret = {}
    with patch.object(Authorisation, 'create', 
            return_value=ret) as mck_create:
        authorisation = AuthorisationRestView(context.request)
        result = authorisation.create()
        assert mck_create.called
        assert result['success'] ==  'Rule successfully created.'

