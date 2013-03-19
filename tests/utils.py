import vault
import sys

_cache = {}


def prompt_for_auth(service):
    global _cache

    if service in _cache:
        return _cache[service]

    original_stdout = sys.stdout
    sys.stdout = sys.stderr
    username = vault.get(service, "username")
    password = vault.get(service, "password")
    sys.stdout = original_stdout

    _cache[service] = (username, password)

    return username, password
