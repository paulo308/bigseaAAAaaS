
from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
from aaa_manager.accounting import Accounting
from aaa_manager.basedb import BaseDB

#Scenario: Create record
@given('I have correct username, message and category')
def step_impl(context):
    context.username = 'teste'
    context.msg = 'test message'
    context.category = 'test'
    context.record = {
            'msg': context.msg,
            'category': context.category,
            }

@when('I create accounting')
def step_impl(context):
    pass

@then('I create record successfully')
def step_impl(context):
    with patch.object(BaseDB, 'insert',
            return_value=True) as mck_insert:
        accounting = Accounting()
        accounting.register(
                context.username, 
                context.msg, 
                context.category)
        assert mck_insert.called
    
