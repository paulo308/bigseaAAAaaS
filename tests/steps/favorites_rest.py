
from unittest.mock import MagicMock
from unittest.mock import patch
from behave import given, when, then
import requests
from collections import namedtuple
from aaa_manager.favorites import Favorites
from aaa_manager.api.favorites import FavoritesRestView


@given('I have correct query string parameters username and favorite')
def step_impl(context):
    context.username = 'teste'
    context.favorite = 'favorite@teste.com'
    context.favorite_info = {
            'favorite': context.favorite,
            }

@when('I call create favorite RESP API service')
def step_impl(context):
    pass

@then('I receive expected success response from favorite association')
def step_impl(context):
    payload = {
            'username': 'teste',
            'item_id': 'a',
            'item_type': 'b',
            'city_id': 1,
            'country_id': 2,
            'favorite_id': 'a',
            'data': 'ab',
            'token': 'bla',
            }
    context.request = context.request(context.settings, params=payload)
    ret = {}
    with patch.object(Favorites, 'create', 
            return_value=ret) as mck_create:
        favorites = FavoritesRestView(context.request)
        result = favorites.create()
        assert mck_create.called
        assert result['success'] ==  'Favorite association successfully created.'

