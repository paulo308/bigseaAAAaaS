"""
Provides access to database collections. Methos to do CRUD operations on user
information. 
"""
import logging

from aaa_manager.db_client import DBClient

LOG = logging.getLogger(__name__)

_DEFAULT_DB_HOST = 'mongo'
_DEFAULT_DB_PORT = 27017
_DEFAULT_DB_NAME = 'AAADB'


class BaseDB:
    """ 
    Provides an interface to use database.
    """

    def __init__(self, host=_DEFAULT_DB_HOST, port=_DEFAULT_DB_PORT):
        self.host = host
        self.port = port
        self.db_client = None

    def _connect(self):
        self.db_client = DBClient(self.host, self.port)
        self.db_client.connect()
        self.db_client.use_db(_DEFAULT_DB_NAME)

    def _close(self):
        self.db_client.close()
    
    def get_all(self, collection):
        """
        Finds all items in `collection`.

        Args:
            collection (str): collection to be searched.

        Returns: 
            result (obt): mongodb result object.
        """
        self._connect()
        result = self.db_client.find(collection, {})
        self._close()
        return result


    def get(self, collection, key, value):
        """
        Finds all items whose `key` field is equal to `value` in `collection`.

        Args:
            collection (str): collection to be searched;
            key (str): name of field to be searched;
            value (str): value to be searched.
   
        Returns: 
            result (obt): mongodb result object.
        """
        self._connect()
        condition = {key: value}
        result = self.db_client.find(collection, condition)
        self._close()
        return result

    def insert(
            self, 
            collection, 
            search_key, 
            search_val, 
            insert_key, 
            insert_val):
        """
        Inserts `item` into `insert_list` list whose `search_key` field value 
        is `search_val`.

        Args:
            collection (str): collection to be searched and inserted/updated;
            search_key (str): name of field to be searched;
            search_val (str): value to be searched;
            insert_key (str): name of the list field in which `insert_val` will
            be inserted;
            insert_val (str): the element to be inserted in the list.
        
        Returns: 
            result (obt): mongodb result object.
        """
        self._connect()
        result = None
        condition = {search_key: search_val}
        output = list(self.db_client.find(collection, condition))

        # if a search for `search_val` returns an empty list, insert new 
        # element
        if len(output) == 0:
            data = {search_key: search_val, insert_key: [insert_val]}
            result = self.db_client.insert(collection, data)
        # else if `insert_val` is not already in `insert_key` list, insert it
        else:
            condition = {search_key: search_val, 
                         insert_key: {"$nin": [insert_val]}}
            new_item = {insert_key: insert_val}
            result = self.db_client.db[collection]\
                .update_many(condition, {"$push": new_item})
        self._close()
        return result

    def update(
            self, 
            collection, 
            search_key, 
            search_val, 
            update_key, 
            old_item,
            new_item):
        """
        Updates `old_item` for `new_item` into `update_key` list whose
        `search_key` value is `search_id`.

        Args:
            collection (str): collection to be searched;
            search_key (str): name of field to be searched;
            search_val (str): value to be searched, so that `old_item` will be 
            replaced for `new_item`;
            update_key (str): name of the list field in which `old_item` will 
            be replaced;
            old_item (str): element to be replaced;
            new_item (str): new element to replace old element.

        Returns:
            result (obt): mongodb result object.
        """
        self._connect()
        condition = {search_key: search_val, update_key: {'$in': [{'username': old_item['username']}]}}
        result = self.db_client.db[collection]\
                     .update_many(condition, 
                                  {"$set": new_item})
        self._close()
        return result.modified_count

    def remove_list_item(
            self, 
            collection, 
            search_key, 
            search_val, 
            remove_key,
            remove_val):
        """
        Removes `remove_val` item from `remove_key` list whose `search_key` 
        field value is `search_val`.

        Args:
            collection (str): collection to be searched;
            search_key (str): name of field to be searched;
            search_val (str): value to be searched, so that `remove_item` will
            be removed into it;
            remove_key (str): name of the list field from which `remove_item`
            will be removed;
            remove_val (str): the element to be removed.

        Returns:
            count (int): number of removed items.
        """
        self._connect()
        condition = {
                search_key: search_val 
                }
        result = self.db_client.db[collection].update_many(
                condition, 
                {
                    "$pull": {
                        remove_key: remove_val 
                        }
                    }
                )
        self._close()
        return result.modified_count

    def remove(self, collection, search_key, search_val):
        """
        Removes the whole list whose `search_key` field value is `search_val`.

        Args:
            collection (str): collection to be searched;
            search_key (str): name of field to be searched;
            search_val (str): value to be searched, such that its list will be
            removed.

        Returns:
            count (int): number of items removed.
        """
        self._connect()
        condition = {search_key: search_val}
        result = self.db_client.db[collection].remove(condition)
        self._close()
        return result['n']

    def verify(self, collection, search_key, search_val, verify_key, verify_val):
        """
        Verifies if `verify_val` item belongs to the `verify_key` list
        whose `search_key` value is `search_val`.

        Args:
            collection (str): collection to be searched;
            search_key (str): name of field to be searched;
            search_val (str): value to be searched, so that `verify_val` item
            will be verified;
            verify_key (str): name of the list field in which `verify_val` item
            will be verified;
            verify_val (str): the element to be verified.

        Returns:
            belongs (bool): True if item belongs to collection and False
            otherwise.
        """
        self._connect()
        condition = {search_key: search_val, verify_key: {"$in": [verify_val]}}
        result = self.db_client.db[collection].find(condition).count()
        self._close()
        return result > 0

    def drop(self, collection):
        """
        Drops the entire `collection` from database.

        Args:
            collection (str): name of collection to be dropped.
        """
        self._connect()
        self.db_client.db[collection].drop()
        self._close()
        return
