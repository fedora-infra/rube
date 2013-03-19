import getpass
import sys

_cache = {}


def prompt_for_auth(key):
    global _cache

    if key in _cache:
        return _cache[key]

    original_stdout = sys.stdout
    sys.stdout = sys.stderr
    username = raw_input(key + " username:")
    sys.stdout = original_stdout
    password = getpass.getpass(key + " password:")

    _cache[key] = (username, password)

    return username, password
