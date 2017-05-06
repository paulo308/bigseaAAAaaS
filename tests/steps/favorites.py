
from aaa_manager.authentication import AuthenticationManager
from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
from aaa_manager.favorites import Favorites
from aaa_manager.basedb import BaseDB

#Scenario: Create favorite
@given('I have correct username and favorite')
def step_impl(context):
    context.username = 'teste'
    context.favorite_info = {
            'item_id': 'a',
            'item_type': 'b',
            'city_id': 1,
            'country_id': 2,
            'favorite_id': 'a',
            'data': 'ab',
            'token': 'bla'
            }

@when('I create favorite')
def step_impl(context):
    pass

@then('I create favorite successfully')
def step_impl(context):
    with patch.object(AuthenticationManager, 'verify_token',
            return_value=True) as mck_ver:
        with patch.object(BaseDB, 'insert',
                return_value=True) as mck_insert:
            favorites = Favorites()
            favorites.create(
                    "2",
                    context.username, 
                    context.favorite_info['item_id'],
                    context.favorite_info['item_type'],
                    context.favorite_info['city_id'],
                    context.favorite_info['country_id'],
                    context.favorite_info['favorite_id'],
                    context.favorite_info['data'],
                    context.favorite_info['token']
                    )
            assert mck_insert.called
            assert mck_ver.called
    
#Scenario: Read favorite
@given('I have correct username and city id and country_id')
def step_impl(context):
    context.username = 'teste'
    context.input_info = {
            'city_id': 1,
            'country_id': 2,
            'token': 'bla'
            }

@when('I read favorite')
def step_impl(context):
    context.favorite_info = [{'favorites': [{
            'item_id': 'a',
            'item_type': 'b',
            'city_id': 1,
            'country_id': 2,
            'favorite_id': 'a',
            'data': 'ab'
            }]}]


@then('I read favorite successfully')
def step_impl(context):
    with patch.object(AuthenticationManager, 'verify_token',
            return_value=True) as mck_ver:
        with patch.object(BaseDB, 'get',
                return_value=context.favorite_info) as mck_get:
            favorites = Favorites()
            result = favorites.read(
                    "2",
                    context.username, 
                    context.input_info['city_id'],
                    context.input_info['country_id'],
                    context.input_info['token']
                    )
            assert mck_get.called
            assert result['item_id'] == 'a'


#Scenario: Delete favorite
@given('I have correct username and favorite id')
def step_impl(context):
    context.username = 'teste'
    context.input_info = {
            'item_id': 'a',
            'token': 'bla'
            }

@when('I delete favorite')
def step_impl(context):
    pass

@then('I delete favorite successfully')
def step_impl(context):
    with patch.object(AuthenticationManager, 'verify_token',
            return_value=True) as mck_ver:
        with patch.object(BaseDB, 'get', return_value=[{'favorites':[{'item_id': 'a'}]}]) as mck_get:
            with patch.object(BaseDB, 'remove_list_item', return_value=1) as mck_del:
                favorites = Favorites()
                result = favorites.delete(
                        "2",
                        context.username, 
                        context.input_info['item_id'],
                        context.input_info['token'],
                        )
            assert mck_get.called
            assert mck_del.called
            assert result != None 


