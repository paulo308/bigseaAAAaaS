"""
Accounting module is responsible for managing loogging information and
generating reports.
"""

import logging
from datetime import datetime
import hashlib

from aaa_manager.basedb import BaseDB

ACCOUNTING_COLLECTION = 'Accounting'
ACCOUNTING_KEY = 'user'
ACCOUNTING_ITEM = 'log'
INFO = "INFO"

LOG = logging.getLogger(__name__)

class Accounting():
    """
    This class is responsible for providing methods to manage resource usage by
    user.
    """

    def __init__(self):
        self.basedb = BaseDB()

    def register(self, user, msg, category):
        """
        Insert accounting information on database.
        """
        LOG.info('accounting.msg: %s' % msg)
        tnow = datetime.now().strftime("%I:%M%p on %B %d, %Y")
        log = {
                'msg': msg, 
                'timestamp': tnow,
                'category': category,
                }
        res = self.basedb.insert(ACCOUNTING_COLLECTION, 
                           ACCOUNTING_KEY, 
                           user, 
                           ACCOUNTING_ITEM, 
                           log)
        return res
        

    def get(self, user):
        """
        Get accounting information from database.
        """
        result = list(self.basedb.get(
            ACCOUNTING_COLLECTION, 
            ACCOUNTING_KEY,
            user))
        for item in result:
            del item['_id']
        return result
