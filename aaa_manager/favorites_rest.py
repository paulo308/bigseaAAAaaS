"""
This file contains the Favorites REST interface. 
"""
import logging

from aaa_manager import Route
from aaa_manager.favorites import Favorites
from pyramid.view import view_config

LOG = logging.getLogger(__name__)


class FavoritesRestView:
    """
    Implements favorites REST API.
    """

    def __init__(self, request):
        self.request = request
        self._settings = request.registry.settings
        self._data = self._settings['data']
        self.favorites = Favorites()

    @view_config(route_name=Route.CREATE_FAVORITE,
                 request_method='POST',
                 renderer='json')
    def create(self):
        """ 
        This method is called from **/engine/api/create_favorite**.
        This method is used to create favorite association.

        Arguments:
            username (str): the username;
            favorite_info (dict): favorite information.

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        username = self.request.params['username']
        favorite_info = self.request.params['favorite_info']
        auth = self.favorites.create(username, favorite_info)
        if auth is not None:
            return {'success': 'Favorite association successfully created.'}
        else:
            return {'error':  'Invalid favorite.'}
            
    @view_config(route_name=Route.READ_FAVORITE,
                 request_method='POST',
                 renderer='json')
    def read(self):
        """ 
        This method is called from **/engine/api/read_favorite**.
        This method is used to read favorite association.

        Arguments:
            username (str): the username;
            city_id (int): city id (external);
            country_id (int): country id (external).

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        username = self.request.params['username']
        city_id = self.request.params['city_id']
        country_id = self.request.params['country_id']
        fav = self.favorites.read(username, city_id, country_id)
        if fav is not None and 'data' in fav:
            return {'success': 'Favorite association successfully created.',
                    'data': fav['data']
                    }
        else:
            return {'error':  'Invalid favorite.'}
    
    @view_config(route_name=Route.DELETE_FAVORITE,
                 request_method='POST',
                 renderer='json')
    def delete(self):
        """ 
        This method is called from **/engine/api/delete_favorite**.
        This method is used to delete favorite association.

        Arguments:
            username (str): the username;
            item_id (int): country id (external).

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        username = self.request.params['username']
        item_id = self.request.params['item_id']
        fav = self.favorites.delete(username, item_id)
        if fav is not None:
            return {'success': 'Favorite association successfully created.'}
        else:
            return {'error':  'Invalid favorite.'}
