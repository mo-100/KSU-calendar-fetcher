import datetime as dt
from os import path

# date
LAST_STUDY_DAY = dt.datetime(2024, 12, 7 + 1)

#  cache
CACHE_DIR = path.abspath('cache')
CACHE_FILE = path.join(CACHE_DIR, 'cache.pkl')
