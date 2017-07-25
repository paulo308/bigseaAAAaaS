"""
This file contains the Favorites REST interface. 
"""
import logging

from aaa_manager.basedb import BaseDB
from aaa_manager import Route
from aaa_manager.favorites import Favorites
from aaa_manager.authentication import AuthenticationManager
from aaa_manager.token import Token
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
        self.authentication = AuthenticationManager()
        self.token = Token()

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
        msg = ''
        try:
            username = self.request.params['username']
            item_id = self.request.params['item_id']
            item_type = self.request.params['item_type']
            city_id = int(self.request.params['city_id'])
            country_id = int(self.request.params['country_id'])
            favorite_id = self.request.params['favorite_id']
            data = self.request.params['data']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                auth = self.favorites.create(
                        2,
                        username, 
                        item_id,
                        item_type,
                        city_id,
                        country_id,
                        favorite_id,
                        data,
                        token)
                if auth is not None:
                    return {'success': 'Favorite association successfully created.'}
                else:
                    return {'error':  'Invalid favorite.'}
            else:
                return {'error':  'Invalid token'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
            
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
        msg = ''
        try:
            username = self.request.params['username']
            city_id = int(self.request.params['city_id'])
            country_id = int(self.request.params['country_id'])
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                fav = self.favorites.read(2, username, city_id, country_id, token)
                if fav is not None and 'data' in fav:
                    return {'success': 'Favorite association successfully read.',
                            'data': fav['data']
                            }
                else:
                    return {'error':  'Invalid favorite.'}
            else:
                return {'error':  'Invalid token'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
    
    @view_config(route_name=Route.READ_FAVORITES,
                 request_method='POST',
                 renderer='json')
    def read_all(self):
        """ 
        This method is called from **/engine/api/read_favorites**.
        This method is used to read favorite association.

        Arguments:
            username (str): the username;

        Returns:
            success (bool): True if sucessfully created and False
            otherwise;
            error (str): an error message if an error occured and an empty
            string otherwise.
        """
        msg = ''
        try:
            username = self.request.params['username']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token':
                if usr == username:
                    fav = self.favorites.read_all(2, username)
                    LOG.info('#### fav: %s' % fav)
                    if fav is not None:
                        return {'success': 'Favorite association successfully read.',
                                'data': fav
                                }
                    else:
                        return {'error':  'Invalid favorite.'}
                else:
                    return {'error': 'Invalid username.'}
            else:
                return {'error':  'Invalid token'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
    
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
        msg = ''
        try:
            username = self.request.params['username']
            item_id = self.request.params['item_id']
            token = self.request.params['token']
            usr = self.token.verify_token(2, token)
            if usr != 'invalid token' and usr == username:
                fav = self.favorites.delete(2, username, item_id, token)
                if fav is not None:
                    return {'success': 'Favorite association successfully deleted.'}
                else:
                    return {'error':  'Invalid favorite.'}
            else:
                return {'error':  'Invalid token'}
        except KeyError as e:
            msg = 'Missing mandatory parameter: ' + str(e)
            raise e
        except Exception as e:
            msg = 'Unknown error occurred: ' + str(e)
            raise e
        LOG.info(msg)
        return {'error': msg}
    
