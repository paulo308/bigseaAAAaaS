
from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
from aaa_manager.favorites import Favorites
from aaa_manager.basedb import BaseDB

#Scenario: Create favorite
@given('I have correct username and favorite')
def step_impl(context):
    context.username = 'teste'
    context.favorite = 'favorite@teste.com'
    context.favorite_info = {
            'favorite': context.favorite
            }

@when('I create favorite')
def step_impl(context):
    pass

@then('I create favorite successfully')
def step_impl(context):
    with patch.object(BaseDB, 'insert',
            return_value=True) as mck_insert:
        favorites = Favorites()
        favorites.create(
                context.username, 
                context.favorite_info)
        assert mck_insert.called
    
