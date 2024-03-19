from functools import wraps

from openfeature import api

from django_openfeature.provider import DjangoTestProvider

__all__ = ["override_feature"]


def override_feature(name, value):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # NOTE: using undocumented client property to access the provider
            provider = api.get_client().provider
            if not isinstance(provider, DjangoTestProvider):
                raise ValueError(
                    "The override_feature decorator requires a DjangoTestProvider to be set."
                )
            provider.push_overrides({name: value})
            try:
                return func(*args, **kwargs)
            finally:
                provider.pop_overrides()

        return wrapper

    return decorator
