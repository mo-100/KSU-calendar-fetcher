from fetcher.utils.config import REPLACE_LIST


def apply_replaces(title: str):
    for old, new in REPLACE_LIST:
        title = title.replace(old, new)
    return title