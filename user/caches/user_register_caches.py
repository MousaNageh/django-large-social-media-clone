from django.core.cache import cache


class UserRegisterCaches:
    _cache_prefix = "user_email_username_"
    cache_lifetime = 60 * 60  # one hour

    @classmethod
    def set_cache(cls, username_or_email):
        cache.set(cls.get_key(username_or_email), 1, timeout=cls.cache_lifetime)
        return 1

    @classmethod
    def get_cache(cls, username_or_email):
        return cache.get(cls.get_key(username_or_email))

    @classmethod
    def get_or_set(cls, username_or_email):
        created = False
        key = cls.get_cache(username_or_email)
        data = cls.get_cache(key)
        if not data:
            created = True
            data = cls.set_cache(username_or_email)
        return data, created

    @classmethod
    def get_key(cls, value):
        return cls._cache_prefix + str(value)
