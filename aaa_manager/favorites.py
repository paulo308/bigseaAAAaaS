"""
Email class is responsible for managing favorite information associated to a 
certain user, which will be identified by username.

"""
from aaa_manager.authentication import _DEFAULT_DB_HOST, _DEFAULT_DB_PORT
from aaa_manager.basedb import BaseDB
from jsonschema import validate, ValidationError
import logging


LOG = logging.getLogger(__name__)
FAVORITE_COLLECTION = 'Authorisation'
FAVORITE_KEY = 'username'
FAVORITE_ITEM = 'favorites'

class Favorites:

    def __init__(self, host=_DEFAULT_DB_HOST, port=_DEFAULT_DB_PORT):
        self.host = host
        self.port = port
        self.basedb = BaseDB(host, port)

    def create(self, username, item_id, item_type, city_id, country_id, favorite_id, data):
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
                }
        if self.validate_favorite(item):
            return self.basedb.insert(
                    FAVORITE_COLLECTION,
                    FAVORITE_KEY,
                    username,
                    FAVORITE_ITEM,
                    item)
        return None

    def read(self, username, city_id, country_id):
        """
        Read favorite information for username. 

        Args: 
            username (str): username;
            city_id (dict): city_id (external);
            ccountry_id (dict): country_id (external).
            
        """
        result = self.basedb.get(
                FAVORITE_COLLECTION, 
                FAVORITE_KEY,
                username)
        for item in result:
            if item['city_id'] == city_id and\
                    item['country_id'] == country_id:
                return item
        return None

    def update(self, username, item_id):
        pass

    def delete(self, username, item_id):
        """
        Delete favorite from database.

        Args:
            username (str): username;

        """
        result = self.basedb.get(
                FAVORITE_COLLECTION, 
                FAVORITE_KEY,
                username)
        for item in result:
            if item['item_id'] == item_id:
                r = self.basedb.remove_list_item(
                        FAVORITE_COLLECTION, 
                        FAVORITE_KEY, 
                        username, 
                        FAVORITE_ITEM, 
                        item)
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
