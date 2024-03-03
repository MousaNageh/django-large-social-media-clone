from django.core.cache import cache


class UserRegisterCaches:
    _cache_prefix = "user_register_email_username_"

    @classmethod
    def set_cache(cls, username_or_email, is_active=False):
        data = {
            "username_or_email": username_or_email,
            "is_active": is_active
        }
        cache.set(cls.get_key(username_or_email), data)
        return data

    @classmethod
    def get_cache(cls, username_or_email):
        return cache.get(cls.get_key(username_or_email))

    @classmethod
    def get_or_set(cls, username_or_email, is_active=False):
        key = cls.get_cache(username_or_email)
        data = cls.get_cache(key)
        if not data:
            return cls.set_cache(username_or_email, is_active)
        return data

    @classmethod
    def get_key(cls, value):
        return cls._cache_prefix + str(value)
