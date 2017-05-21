"""
Database client implementation. In this file there are methods to access mongo
database. DBClient class encapsulates the client component that is responsible
for establishing connections with MongoDB. 
"""
import logging
import ssl

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from aaa_manager.exceptions import DBError

LOG = logging.getLogger(__name__)

_DEFAULT_DB_HOST = 'mongo'
_DEFAULT_DB_PORT = 27017
_DEFAULT_DB_NAME = 'AAADB'
_DEFAULT_CLIENT_CERT = 'certs/mongo_client_crt.pem'
_DEFAULT_CA_CERT = 'certs/root_ca.pem'
_DEFAULT_USER = 'OU=mongo_client,O=Bigsea,L=Campinas,ST=SP,C=BR'
_DEFAULT_MECHANISM = 'MONGODB-X509'


class DBClient:
    """
    Provides an interface to use the database.
    """

    def __init__(self, host=_DEFAULT_DB_HOST, port=_DEFAULT_DB_PORT):
        self.host = host
        self.port = port
        self.name = None
        self.client = None
        self.db = None

    def connect(self):
        """
        Connects to MongoDB.
        """
        try:
            self.client = MongoClient(self.host,
                                      self.port,
                                      ssl=True,
                                      ssl_certfile=_DEFAULT_CLIENT_CERT,
                                      ssl_cert_reqs=ssl.CERT_REQUIRED,
                                      ssl_ca_certs=_DEFAULT_CA_CERT)
            """self.client = MongoClient(self.host,
                                      self.port,
                                      ssl=False)"""
        except ConnectionFailure as e:
            raise DBError("Can't connect to database.") from e

    def use_db(self, name=_DEFAULT_DB_NAME):
        """
        Uses database given by `name`.
        """
        self.name = name
        self.db = self.client[name]
        self.db.authenticate(_DEFAULT_USER, mechanism=_DEFAULT_MECHANISM)

    def insert(self, collection, data):
        """
        Inserts `data` into `collection`.
        """
        result = self.db[collection].insert_one(data)
        return result.inserted_id

    def find(self, collection, condition):
        """
        Finds all items in `collection` respecting `condition`.
        """
        return self.db[collection].find(condition)

    def remove(self, collection, condition):
        """
        Removes all items in `collection` respecting `condition`.
        """
        result = self.db[collection].delete_many(condition)
        return result.deleted_count

    def close(self):
        """
        Closes connection.
        """
        self.client.close()
