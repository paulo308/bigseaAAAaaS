"""
Email class is responsible for managing favorite information associated to a 
certain user, which will be identified by username.

"""
from aaa_manager.basedb import BaseDB
from aaa_manager.token import Token
from jsonschema import validate, ValidationError
import logging


LOG = logging.getLogger(__name__)
FAVORITE_COLLECTION = 'Favorites'
FAVORITE_KEY = 'username'
FAVORITE_ITEM = 'favorites'

class Favorites:

    def __init__(self):
        self.basedb = BaseDB()

    def create(self, app_id, username, item_id, item_type, city_id, country_id, favorite_id, data, token):
        """
        Create an favorite associated to username on database. 

        Args:
            username (str): username;
            item_id: item id (primary key),
            item_type: item_type (distinguish among applications),
            city_id: city_id (external),
            country_id: country_id (external),
            favorite_id: favorite_id (external),
            data: data (external),
            token (str): token.

        Returns:
            database response
        """
        item = {
                'item_id': item_id,
                'item_type': item_type,
                'city_id': city_id,
                'country_id': country_id,
                'favorite_id': favorite_id,
                'data': data,
                'token': token,
                }
        if self.validate_favorite(item):
            return self.basedb.insert(
                    FAVORITE_COLLECTION,
                    FAVORITE_KEY,
                    username,
                    FAVORITE_ITEM,
                    item)
        return None

    def read(self, app_id, username, city_id, country_id, token):
        """
        Read favorite information for username. 

        Args: 
            username (str): username;
            city_id (dict): city_id (external);
            ccountry_id (dict): country_id (external);
            token (str): token.
            
        """
        result = self.basedb.get(
                FAVORITE_COLLECTION, 
                FAVORITE_KEY,
                username)
        for item in result:
            for elem in item['favorites']:
                if elem['city_id'] == city_id and\
                        elem['country_id'] == country_id:
                    return elem
        return None
    
    def read_all(self, app_id, username):
        """
        Read favorites information for username. 

        Args: 
            username (str): username;
            city_id (dict): city_id (external);
            ccountry_id (dict): country_id (external);
            token (str): token.
            
        """
        result = self.basedb.get(
                FAVORITE_COLLECTION, 
                FAVORITE_KEY,
                username)
        res = list(result)
        for item in res:
            del item['_id']
        return res

    def update(self, username, item_id):
        pass

    def delete(self, app_id, username, item_id, token):
        """
        Delete favorite from database.

        Args:
            username (str): username;
            item_id (str): item primary key (external);
            token (str): token.

        """
        result = self.basedb.get(
                FAVORITE_COLLECTION, 
                FAVORITE_KEY,
                username)
        for item in result:
            for elem in item['favorites']:
                if elem['item_id'] == item_id:
                    r = self.basedb.remove_list_item(
                            FAVORITE_COLLECTION, 
                            FAVORITE_KEY, 
                            username, 
                            FAVORITE_ITEM, 
                            elem)
                    return r
        return None

    
    def validate_favorite(self, favorite_info):
        SCHEMA = {
                    'type': 'object',
                    'properties': 
                    {
                        'item_id': {'type': 'string'},
                        'item_type': {'type': 'string'},
                        'city_id': {'type': 'number'},
                        'country_id': {'type': 'number'},
                        'favorite_id': {'type': 'string', 'maxLength': 4000},
                        'data': {'type': 'string', 'maxLength': 10000},
                    },
                    'required' : ['item_id', 'item_type', 'city_id', 'country_id', 'favorite_id', 'data']
                }
        try:
            validate(favorite_info, SCHEMA)
        except ValidationError as err:
            LOG.error('Invalid favorite')
            raise Exception('Invalid favorite') from err 
        return True
