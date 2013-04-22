# dumpmon.py
# Author: Jordan Wright
# Version: 0.0 (in dev)

from lib.Pastebin import Pastebin, PastebinPaste
from lib.Slexy import Slexy, SlexyPaste
from lib.Pastie import Pastie, PastiePaste
from settings import USE_DB, DB_HOST, DB_PORT
from pymongo import MongoClient
from time import sleep
import threading
import logging
import argparse

def setup():
    if USE_DB:
        db_client = MongoClient(DB_HOST, DB_PORT).paste_db
        db_client.pastes.create_index("url", unique=True, dropDups=True)
        db_client.urls.create_index("url", unique=True, dropDups=True)

def monitor():
    setup()
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="more verbose", action="store_true")
    args = parser.parse_args()
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',  level=level)
    logging.info('Monitoring...')

    log_lock = threading.Lock()
    tweet_lock = threading.Lock()

    pastebin_thread = threading.Thread(target=Pastebin().monitor, args=[tweet_lock])
    slexy_thread = threading.Thread(target=Slexy().monitor, args=[tweet_lock])
    pastie_thead = threading.Thread(target=Pastie().monitor, args=[tweet_lock])

    for thread in (pastebin_thread, slexy_thread, pastie_thead):
        thread.daemon = True
        thread.start()

    try:
        while(1):
            sleep(5)
    except KeyboardInterrupt:
        logging.warn('Stopped.')


if __name__ == "__main__":
    monitor()
