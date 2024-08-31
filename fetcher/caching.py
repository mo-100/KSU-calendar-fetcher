import os
import pickle
from typing import Callable

from fetcher.constants import CACHE_DIR, CACHE_FILE


def use_cache(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        init_dir(CACHE_DIR)
        # check cache
        item = read_cache()
        if item:
            return item

        # if no cache then fetch
        item = func(*args, **kwargs)

        # write cache then return
        write_cache(item)
        return item

    return wrapper


def init_dir(path: str):
    if not os.path.isdir(path):
        os.makedirs(path)


def write_cache(item):
    print('writing cache')
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(item, f)


def clear_cache():
    print('clearing cache')
    os.remove(CACHE_FILE)


def read_cache():
    print('reading cache')
    if not os.path.isfile(CACHE_FILE):
        print('no cache found')
        return None

    with open(CACHE_FILE, 'rb') as f:
        return pickle.load(f)
