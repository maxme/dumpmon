import time
import datetime
import logging
import pymongo
from settings import USE_DB, DB_HOST, DB_PORT
from collections import deque

class Site(deque):
    def __init__(self):
        self.db_pastes = pymongo.MongoClient(DB_HOST, DB_PORT).paste_db.pastes
        self.db_urls = pymongo.MongoClient(DB_HOST, DB_PORT).paste_db.urls

    def empty(self):
        return len(self) == 0

    def monitor(self, t_lock):
        self.update()
        while True:
            while not self.empty():
                paste = self.pop()
                if self.db_urls.find_one({'url': paste.url}):
                    continue
                self.db_urls.save({'url': paste.url})
                self.ref_id = paste.id
                logging.info('Checking ' + paste.url)
                paste.text = self.get_paste_text(paste)
                matched = paste.match()
                if matched and USE_DB:
                    with t_lock:
                        try:
                            self.db_pastes.save({
                                'url': paste.url,
                                'text': paste.text,
                                'matches': paste.matches,
                                'date': datetime.datetime.utcnow(),
                            })
                        except pymongo.errors.DuplicateKeyError:
                            pass
            time.sleep(self.sleep)
            self.update()
