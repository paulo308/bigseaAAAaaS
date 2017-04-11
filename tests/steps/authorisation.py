
from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
from aaa_manager.authorisation import Authorisation
from aaa_manager.basedb import BaseDB

#Scenario: Create rule
@given('I have correct username, resource name and rule')
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

@when('I create authorisation')
def step_impl(context):
    pass

@then('I create rule successfully')
def step_impl(context):
    with patch.object(BaseDB, 'insert',
            return_value=True) as mck_insert:
        authorisation = Authorisation()
        authorisation.create(
                context.username, 
                context.resource_name, 
                context.rule)
        assert mck_insert.called
    
