"""
Accounting module is responsible for managing loogging information and
generating reports.
"""

import logging
import time
import hashlib

ACCOUNTING_COLLECTION = 'Accounting'
ACCOUNTING_KEY = 'user'
ACCOUNTING_ITEM = 'log'
INFO = "INFO"

class Accounting():

    def __init__(self):
        self.basedb = BaseDB()

    def insert(self, user, msg, category):
        LOG.info(msg)
        log = {
                'msg': msg, 
                'timestamp': time.now(),
                'hash': hashlib.sha512(msg.encode()).hexdigest(),
                'category': category,
                }
        res = self.basedb.insert(ACCOUNTING_COLLECTION, 
                           ACCOUNTING_KEY, 
                           user, 
                           ACCOUNTING_ITEM, 
                           log)
        return res
        

    def get(self, user, category):
        response = []
        result = self.basedb.get(ACCOUNTING_COLLECTION, ACCOUNTING_KEY, user)
        for item in result:
            if item['category'] == category:
                response.append(response, item)
        return response
