import os
import hashlib

CACHE_DIR = ".cache"


def cache_get(url):
    path = _path(url)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read(), True
    return None, False


def cache_set(url, content):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(_path(url), "w", encoding="utf-8") as f:
        f.write(content)


def _path(url):
    h = hashlib.md5(url.encode()).hexdigest()
    return os.path.join(CACHE_DIR, h + ".txt")
