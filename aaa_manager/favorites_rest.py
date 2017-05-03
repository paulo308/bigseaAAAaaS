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

    @view_config(route_name=Route.CREATE_EMAIL,
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
            
