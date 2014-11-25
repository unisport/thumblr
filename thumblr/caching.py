from django.core.cache import get_cache, cache, InvalidCacheBackendError


try:
    thumblr_cache = get_cache('thumblr')
except InvalidCacheBackendError:
    thumblr_cache = cache

# pinging on cache
thumblr_cache.get("FOO")


def _get_key(f, *args):
    return "{func_name}:{arg}".format(
        func_name=f.func_name,
        arg="_".join(map(str, args)),
    )


def cached(f):
    """Simple cache for functions, cached function **must** get only **positional** arguments, which have unique
    __str__ return value"""

    def cached_f(*args):
        key = _get_key(f, *args)

        val = thumblr_cache.get(key)

        if val:
            return val

        val = f(*args)
        thumblr_cache.set(key, val)

        return val

    cached_f.func_name = f.func_name

    return cached_f


def drop_cache_for(f, *args):
    key = _get_key(f, *args)

    thumblr_cache.delete(key)
